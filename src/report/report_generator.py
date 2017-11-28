
from os import path

import plotly as py
import plotly.graph_objs as graph_objs

class ReportGenerator(object):

    dir_path = path.dirname(path.realpath(__file__))
    report_directory = dir_path + '/../../report/'
    graph_directory = report_directory + 'graphs/'


    def __init__(self, general_info):
        self.general_info = general_info


    def generate_global_graph(self):
        labels = []
        values = []

        for (key, item) in self.general_info.stats.items():
            labels.append(item.name)
            values.append(item.count)

        trace = graph_objs.Pie(labels=labels, values=values)

        graph_path = py.offline.plot([trace],
                         filename=self.graph_directory + 'global_' + self.general_info.file_name + '.html', auto_open=False)
        
        return '''
        <h2> Global info </h2>
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
        src="''' + graph_path + '''"></iframe>'''

    def generate_global_sql_graph(self):
        labels = []
        values = []
        nb_db_requests = 0

        stats = self.general_info.stats
        if('db' in stats.keys()):
            nb_db_requests += stats['db'].count
        if('neutron.db' in stats.keys()):
            nb_db_requests += stats['neutron.db'].count

        trace = graph_objs.Bar(
            x=['Total DB requests', 'Select 1', 'Joins', 'Transactions'],
            y=[nb_db_requests,self.general_info.total_select1,
                 self.general_info.total_joins, self.general_info.total_transactions]
        )

        graph_path = py.offline.plot([trace],
                    filename=self.graph_directory + 'global_sql_' + self.general_info.file_name + '.html', auto_open=False)

        return '''
        <h2> Global SQL info </h2>
        <iframe width="1200" height="550" frameborder="0" seamless="seamless" scrolling="no" \
        src="''' + graph_path + '''"></iframe>'''

    def generate_report(self):
        global_html = self.generate_global_graph()

        globalsql_html = self.generate_global_sql_graph()

        html_string = '''
        <html>
            <head>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                <style>body{ margin:0 100; background:whitesmoke; }</style>
            </head>
            <body>
                <h1>SQL Report for Openstack</h1>
                <h2> File : ''' + self.general_info.file_name + '''

                ''' + global_html + '''
                ''' + globalsql_html + '''
            </body>
        </html>'''

        f = open(self.report_directory + 'report_' + self.general_info.file_name + '.html','w')
        f.write(html_string)
        f.close()
        



# labels = ['label1', 'label2', 'label3']
# values = [200,400,1000]

# trace = graph_objs.Pie(labels=labels, values=values)

# chemin = py.offline.plot([trace], filename='toto1.html', auto_open=False)


# labelsb = ['label1', 'label2', 'label3']
# valuesb = [200,400,1000]

# traceb = graph_objs.Pie(labels=labelsb, values=valuesb)

# cheminb = py.offline.plot([traceb], filename='toto2.html', auto_open=False)

# html_string = '''
# <html>
#     <head>
#         <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
#         <style>body{ margin:0 100; background:whitesmoke; }</style>
#     </head>
#     <body>
#         <h1>2014 technology and CPG stock prices</h1>

#         <!-- *** Section 1 *** -->
#         <h2>Section 1: Apple Inc. (AAPL) stock in 2014</h2>
#         <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
# src="''' + chemin + '''"></iframe>
#         <p>Apple stock price rose steadily through 2014.</p>
        
#         <!-- *** Section 2 *** -->
#         <h2>Section 2: AAPL compared to other 2014 stocks</h2>
#         <iframe width="1000" height="1000" frameborder="0" seamless="seamless" scrolling="no" \
# src="''' + cheminb + '''"></iframe>
#     </body>
# </html>'''


# # Finally, write the html string to a local file.

# # In[185]:

# f = open('./report.html','w')
# f.write(html_string)
# f.close()