

class GeneralInfo(object):
    """Class representing general information """

    def __init__(self, file_name):
        self.file_name = file_name
        self.stats = dict()
        self.children = []
        self.total_joins = 0
        self.total_transactions = 0

    def add_stat(self, stat):
        self.stats[stat.name] = stat

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        result = ""
        result += '---------------------------\n'
        result += self.file_name + '\n'
        result += '---------------------------\n'
        result += "Total joins : " + str(self.total_joins) + "\n"
        result += "Total transactions : " + str(self.total_transactions) + "\n"
        result += '---------------------------\n'
        for (key, item) in self.stats.items():
            result += str(item) + '\n'
        result += '---------------------------\n'
        for item in self.children:
            result += str(item) + '\n'
        result += '---------------------------\n'
        result += '---------------------------\n'
        result += '---------------------------\n'
        return result
