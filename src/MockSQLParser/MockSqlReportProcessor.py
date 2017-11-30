import sys

from MockSQLParser.SqlReport import SqlReport

class MockSqlReportProcessor:
    JOIN_KEY = "JOIN"
    TRANSACTION_KEY = "BEGIN"

    def report(self, request):
        report = SqlReport()
        report.nb_join += request.count(self.JOIN_KEY)
        report.nb_transac += request.count(self.TRANSACTION_KEY)
        return report

