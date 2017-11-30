from dto.component import Component


class DBComponent(Component):
    types = ['db', 'neutron.db']

    def __init__(self, module, project, duration, parent_id, trace_id,
                 sql_stats, host, params, statement):
        super(DBComponent, self).__init__(module, project, duration,
                                          parent_id, trace_id)
        self.host = host
        self.params = params
        self.statement = statement
        self.sql_stats = sql_stats

    def get_statement(self):
        return self.statement.replace('`', '\`')

    def __str__(self):
        result = "DB_COMPONENT\n"

        result += super(DBComponent, self).__str__()
        result += self.sql_stats.__str__()
        result += "Host : " + self.host + "\n"
        result += "Statement : " + self.statement + "\n"
        result += "{"
        for param in self.params:
            result += param + ", "
        result += "}\n"
        for child in self.children:
            result += child.__str__() + '\n'
        return result
