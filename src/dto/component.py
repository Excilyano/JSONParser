
class Component(object):

    def __init__(self, module, project, duration, parent_id, trace_id):
        self.module = module
        self.project = project
        self.duration = duration
        self.children = []
        self.trace_id = trace_id
        self.parent_id = parent_id

    def add_child(self, child):
        self.children.append(child)

    def get_statement(self):
        return self.project

    def __str__(self):
        result = ""
        result += "Name : " + self.module + "\n"
        result += "Project : " + self.project + "\n"
        result += "Duration : " + self.duration + "\n"
        result += "Trace id : " + self.trace_id + "\n"
        result += "Parent id : " + self.parent_id + "\n"

        return result
