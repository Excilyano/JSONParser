
from datetime import datetime, timedelta
from os import path
from re import search
from utils import Utils

from dto.component import Component
from dto.database_component import DBComponent
from dto.function_component import FunctionComponent
from dto.general_info import GeneralInfo
from dto.http_component import HTTPComponent
from dto.stats import Stats

from report.report_generator import ReportGenerator

from SQLParser.SqlReportProcessor import SqlReportProcessor

from MockSQLParser.MockSqlReportProcessor import MockSqlReportProcessor

import time


class JsonParser(object):
    """Class used to parse Json files from openstack"""
    dir_path = path.dirname(path.realpath(__file__))
    files_directory = dir_path + '/../files/'
    logs_directory = dir_path + '/../output/logs/'
    # sqlreportprocessor = SqlReportProcessor() # Use this project to use antlr parser ; might prove useful if the amount of metrics increase
    sqlreportprocessor = MockSqlReportProcessor() # Use this project to use minimalist SQL reader ; enough with current metrics
    nb_joins = 0
    nb_transactions = 0
    nb_select1 = 0
    duration_joins = timedelta()
    duration_transactions = timedelta()
    duration_select1 = timedelta()
    sql_parsing_duration = 0
    json_parsing_duration = 0
    graph_generation_duration = 0

    def __init__(self):
        self.util = Utils()
        self.files = self.util.find_files(self.files_directory)
        self.json_data = dict()
        self.object_data = dict()
        self.requests = []
        self.initialize_jsondata()

    def initialize_jsondata(self):
        for file in self.files:
            self.json_data[path.basename(file)] = (self.util.read_jsonfile(file))

    def extract_from_json(self):
        time_start = time.time()

        for (key, json) in self.json_data.items():
            self.extract_generalinfo(key, json)
            self.nb_joins = 0
            self.nb_transactions = 0
            self.nb_select1 = 0
            self.duration_joins = timedelta()
            self.duration_transactions = timedelta()
            self.duration_select1 = timedelta()

        self.json_parsing_duration = time.time() - time_start - self.sql_parsing_duration

    def generate_graphs(self):
        time_start = time.time()

        generator = ReportGenerator()
        for file in self.object_data:
            generator.general_info = self.object_data[file]
            generator.generate_report()

        generator.generate_report_index()

        self.graph_generation_duration = time.time() - time_start

    def extract_generalinfo(self, file, json):
        general_info = GeneralInfo(file_name=file)

        for (key, item) in json["stats"].items():
            general_info.add_stat(Stats(name=key,
                                        count=item["count"],
                                        duration=item["duration"]
                                        )
                                  )

        for data in json["children"]:
            self.explore_child(data, general_info)

        general_info.total_nb_joins = self.nb_joins
        general_info.total_nb_transactions = self.nb_transactions
        general_info.total_nb_select1 = self.nb_select1
        general_info.total_duration_joins = self.duration_joins
        general_info.total_duration_transactions = self.duration_transactions
        general_info.total_duration_select1 = self.duration_select1

        self.object_data[file] = general_info
        
        self.generate_log(file, general_info)

    def explore_child(self, child, parent):
        info = child["info"]

        keys = list(info.keys())
        module = ''

        for key in keys:
            module = self.extract_component_from_meta(key)
            if module:
                break

        if module:
            start = info["meta.raw_payload."+module+"-start"]["timestamp"]
            end = info["meta.raw_payload."+module+"-stop"]["timestamp"]

            duration = self.util.convert_string_to_datetime(end) - \
                       self.util.convert_string_to_datetime(start)

            trace_id = child["trace_id"]
            parent_id = child["parent_id"]
            project = info["project"]

            general = Component(
                module=module,
                project=project,
                duration=duration,
                parent_id=parent_id,
                trace_id=trace_id
            )

            if module in DBComponent.types:
                component = self.parse_database_component(general,
                                                          module, info)
            elif module in FunctionComponent.types:
                component = self.parse_function_component(general,
                                                          module, info)
            elif module in HTTPComponent.types:
                component = self.parse_http_component(general,
                                                      module, info)
            else:
                raise ValueError("Key should exist in types")

            parent.add_child(component)

        else:
            raise ValueError("No component found")

        for sub_child in child["children"]:
            self.explore_child(sub_child, component)

    def extract_component_from_meta(self, string):
        result = ''
        found = search("meta.raw_payload.(.+?)-start", string)
        if found:
            result = found.group(1)

        return result

    def parse_database_component(self, general, key, component):
        db = component["meta.raw_payload." + key + "-start"]
        host = db["info"]["host"]
        params = db["info"]["db"]["params"]
        statement = db["info"]["db"]["statement"]

        time_start = time.time()
        sql_stats = self.sqlreportprocessor.report(statement)
        self.sql_parsing_duration += time.time() - time_start

        date_format = "%Mm%Ss.%f"

        if(statement.upper() == "SELECT 1"):
            self.nb_select1 += 1
            self.duration_select1 += general.duration
        else:
            if(sql_stats.nb_join > 0):
                self.nb_joins += 1
                self.duration_joins += general.duration

            if(sql_stats.nb_transac > 0):
                self.nb_transactions += 1
                self.duration_transactions += general.duration

        db_component = DBComponent(
            module=general.module,
            project=general.project,
            duration=general.duration,
            parent_id=general.parent_id,
            trace_id=general.trace_id,
            sql_stats=sql_stats,
            host=host,
            params=params,
            statement=statement
        )

        return db_component

    def parse_function_component(self, general, key, component):

        function = component["meta.raw_payload." + key + "-start"]["info"]\
                            ["function"]["name"]

        fun_component = FunctionComponent(
            module=general.module,
            project=general.project,
            duration=general.duration,
            parent_id=general.parent_id,
            trace_id=general.trace_id,
            function_call=function
        )

        return fun_component

    def parse_http_component(self, general, key, component):
        host = component["host"]

        request = component["meta.raw_payload." + key + "-start"]\
                           ["info"]["request"]

        path = request["path"]
        scheme = request["scheme"]
        method = request["method"]
        query = request["query"]

        http_component = HTTPComponent(
            module=general.module,
            project=general.project,
            duration=general.duration,
            parent_id=general.parent_id,
            trace_id=general.trace_id,
            host=host,
            path=path,
            scheme=scheme,
            method=method,
            query=query
        )

        return http_component

    def generate_log(self, file, general_info):
        with open(self.logs_directory + file + ".log", "w") as output_file:
            output_file.write(general_info.__str__())
            output_file.close()
