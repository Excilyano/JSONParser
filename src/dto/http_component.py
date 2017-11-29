from dto.component import Component


class HTTPComponent(Component):
    types = ['wsgi']

    def __init__(self, module, project, duration, parent_id, trace_id,
                 host, path, scheme, method, query):
        super(HTTPComponent, self).__init__(module, project, duration,
                                            parent_id, trace_id)
        self.host = host
        self.path = path
        self.scheme = scheme
        self.method = method
        self.query = query

    def get_statement(self):
        return self.method + ' => ' + self.path

    def __str__(self):
        result = "HTTP_COMPONENT" + "\n"

        result += super(HTTPComponent, self).__str__()
        result += "Host : " + self.host + "\n"
        result += "Path : " + self.path + "\n"
        result += "Scheme : " + self.scheme + "\n"
        result += "Method : " + self.method + "\n"
        result += "Query : " + self.query + "\n"

        for child in self.children:
            result += child.__str__() + "\n"
        return result
