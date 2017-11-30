
from os import path

import plotly as py
import plotly.graph_objs as graph_objs

from utils import Utils


class ReportGenerator(object):

    dir_path = path.dirname(path.realpath(__file__))
    report_directory = dir_path + '/../../output/report/'
    graph_directory = report_directory + 'graphs/'

    def __init__(self):
        self.util = Utils()

    def generate_global_graph_byrequest(self):
        labels = []
        values = []

        for (key, item) in self.general_info.stats.items():
            labels.append(item.name)
            values.append(item.count)

        trace = graph_objs.Pie(labels=labels, values=values)

        graph_path = py.offline.plot([trace],
                                     filename=self.graph_directory +
                                     'global_by_request_' +
                                     self.general_info.file_name + '.html',
                                     auto_open=False)

        return '''
        <h2> Global info by requests</h2>
        <h4> Proportion of requests executed by each component used \
        in the requested action on OpenStack.</h4>
        <iframe width="1000" height="550" frameborder="0" seamless="seamless"\
        scrolling="no" src="graphs/''' + path.basename(graph_path) + '''"></iframe>'''

    def generate_global_graph_byduration(self):
        labels = []
        values = []

        for (key, item) in self.general_info.stats.items():
            labels.append(item.name)
            values.append(item.duration)

        trace = graph_objs.Pie(labels=labels, values=values)

        graph_path = py.offline.plot([trace],
                                     filename=self.graph_directory +
                                     'global_by_duration_' +
                                     self.general_info.file_name + '.html',
                                     auto_open=False)

        return '''
        <h2> Global info by duration</h2>
        <h4> Time consumption for each component used \
        in the requested action on OpenStack. </h4>
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" \
        scrolling="no" src="graphs/''' + path.basename(graph_path) + '''"></iframe>'''

    def generate_global_sql_graph_byrequest(self):
        nb_dbrequests = 0

        stats = self.general_info.stats
        if('db' in stats.keys()):
            nb_dbrequests += stats['db'].count
        if('neutron.db' in stats.keys()):
            nb_dbrequests += stats['neutron.db'].count

        trace = graph_objs.Bar(
            x=['Total DB requests', 'Select 1', 'Joins', 'Transactions'],
            y=[nb_dbrequests, self.general_info.total_nb_select1,
               self.general_info.total_nb_joins,
               self.general_info.total_nb_transactions]
        )

        graph_path = py.offline.plot([trace],
                                     filename=self.graph_directory +
                                     'global_sql_byrequest_' +
                                     self.general_info.file_name + '.html',
                                     auto_open=False)

        return '''
        <h2> Global SQL info by request</h2>
        <h4> Number of JOIN, SELECT 1 and transactions found in \
        the executed requests from the action performed on OpenStack. </h4>
        <iframe width="1200" height="550" frameborder="0" seamless="seamless" \
        scrolling="no" src="graphs/''' + path.basename(graph_path) + '''"></iframe>'''

    def generate_global_sql_graph_byduration(self):

        duration_db_requests = 0

        ms_select1 = self.general_info.total_duration_select1.total_seconds()*1000 + \
                      self.general_info.total_duration_select1.microseconds/1000

        ms_joins = self.general_info.total_duration_joins.total_seconds()*1000 + \
                      self.general_info.total_duration_joins.microseconds/1000

        ms_transactions = self.general_info.total_duration_transactions.total_seconds()*1000 + \
                      self.general_info.total_duration_transactions.microseconds/1000

        stats = self.general_info.stats
        if('db' in stats.keys()):
            duration_db_requests += stats['db'].duration
        if('neutron.db' in stats.keys()):
            duration_db_requests += stats['neutron.db'].duration

        trace = graph_objs.Bar(
            x=['Total DB requests', 'Select 1', 'Joins', 'Transactions'],
            y=[duration_db_requests, ms_select1, ms_joins, ms_transactions]
        )

        graph_path = py.offline.plot([trace],
                                     filename=self.graph_directory +
                                     'global_sql_byduration' +
                                     self.general_info.file_name + '.html',
                                     auto_open=False)

        return '''
        <h2> Global SQL info by duration</h2>
        <h4> Time consumption of JOIN, SELECT 1 and transactions found in \
        the executed requests from the action performed on OpenStack. </h4>
        <iframe width="1200" height="550" frameborder="0" seamless="seamless" \
        scrolling="no" src="graphs/''' + path.basename(graph_path) + '''"></iframe>'''



    def generate_tree(self):
        html_string = '''
        <script>
        let data = [
            '''

        for item in self.general_info.children:
            html_string += '''
            {
                state: {
                    expanded:false
                },
                text: `[''' + item.project + '''] - ''' + self.util.convert_datetime_to_string(item.duration) + ''' - ''' + item.get_statement() + '''`,
            '''
            if(len(item.children) != 0):
                html_string += 'nodes: ['
                for child in item.children:
                    html_string += self.generate_children_tree(child)
                html_string += ']'

            html_string += '},'

        html_string += '''
        ]
        $('#tree').treeview({data: data});

        </script>
        '''

        return html_string

    def generate_children_tree(self, item):
        html_string = '''
        {
            state: {
                expanded: false
            },
            text: `[''' + item.project + '''] - ''' + self.util.convert_datetime_to_string(item.duration) + ''' - ''' + item.get_statement() + '''`,
        '''

        if(len(item.children) != 0):
            html_string += 'nodes: ['
            for child in item.children:
                html_string += self.generate_children_tree(child)
            html_string += ']'

        html_string += '},'

        return html_string

    def generate_report_index(self):
        files = self.util.find_files(self.report_directory)

        files.remove(self.report_directory + 'index_report.html')

        html_list = ""

        for file in files:
            html_list += '<li><a href="' + path.basename(file) + '">' + path.basename(file) + '</a></li>\n'

        html_string = '''
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-treeview/1.2.0/bootstrap-treeview.min.css">
                <style>body{ margin:0 100; background:whitesmoke; }</style>  
            </head>
            <body>
                <h1>Index of reports for Openstack </h1></br>
                <h4> These documents reports some metrics about SQL requests played during the execution of any action done on OpenStack. </h4>
                </br></br>
                <ul>
                    ''' + html_list + '''
                </ul>
            </body>
        </html>
        '''

        with open(self.report_directory + 'index_report.html', 'w') as f:
            f.write(html_string)
            f.close()

    def generate_report(self):
        global_byrequest_html = self.generate_global_graph_byrequest()

        global_byduration_html = self.generate_global_graph_byduration()

        globalsql_byrequest_html = self.generate_global_sql_graph_byrequest()

        globalsql_byduration_html = self.generate_global_sql_graph_byduration()

        tree_html = self.generate_tree()

        html_string = '''
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-treeview/1.2.0/bootstrap-treeview.min.css">
                <style>body{ margin:0 100; background:whitesmoke; }</style>
            </head>
            <body>
                <h1>SQL Report for Openstack</h1></br>
                <h4> File : ''' + self.general_info.file_name + '''</h4>
                </br></br>
                ''' + global_byrequest_html + '''
                </br></br>
                ''' + global_byduration_html + '''
                </br></br>
                ''' + globalsql_byrequest_html + '''
                </br></br>
                ''' + globalsql_byduration_html + '''
                </br></br>                
                <h2> Tree view of the request calls </h2>
                <h4>This view shows the hierarchy between all the request that have been made throughout this trace</h4>
                </br>
                <div class="row>
                    <div class="col-lg-6">
                        <div class="input-group">
                        <input type="text" id="input-search" class="form-control" placeholder="Filter results" onkeydown="filterInput(event)">
                        <span class="input-group-btn">
                            <button class="btn btn-secondary" id="filter-button" type="button" onclick="filter()">Filter</button>
                        </span>
                        </div>
                    </div>
                </div></br>
                <div id="tree"></div>
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-treeview/1.2.0/bootstrap-treeview.min.js"></script>
            ''' + tree_html + '''

            <script>

            function filter(){
                $('#tree').treeview('collapseAll', { silent: true });
                $('#tree').treeview('search', [document.getElementById('input-search').value, {
                    ignoreCase: true,
                    exactMatch: false,
                    revealResults: true
                }]);
            }

            function filterInput(e){
                if(e.keyCode == 13){
                    filter();
                }
            }

            </script>
            </body>
        </html>'''

        with open(self.report_directory + 'report_' + self.general_info.file_name + '.html', 'w') as f:
            f.write(html_string)
            f.close()
