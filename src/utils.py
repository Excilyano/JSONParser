from datetime import datetime
import json
from os import listdir
from os.path import isfile
from os.path import join


class Utils(object):
    """Utility class """

    def read_jsonfile(self, file_path):
        with open(file_path) as file:
            json_data = json.load(file)
            file.close
            return json_data

    def find_files(self, directory_path):
        return [join(directory_path, file)
                for file in listdir(directory_path)
                if isfile(join(directory_path, file))
                ]

    def convert_string_to_datetime(self, string):
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        return datetime.strptime(string, date_format)

    def convert_datetime_to_string(self, datetime):
        hours = datetime.seconds // 3600
        minutes = (datetime.seconds % 3600) // 60
        seconds = datetime.seconds % 60
        milliseconds = datetime.microseconds // 1000
        microseconds = datetime.microseconds % 1000

        result = ""

        result += str(minutes) + 'm ' if minutes > 0 else ""
        result += str(seconds) + 's ' if seconds > 0 else ""

        return result + str(milliseconds) + 'ms ' + str(microseconds) + 'µs'
