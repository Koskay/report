from dataclasses import astuple

from tabulate import tabulate

from reports.models import ReportData


def display_to_console(report_data: ReportData):
    """Выводит данные отчёта в консоль в виде отформатированной таблицы."""

    table_data = [astuple(item) for item in report_data.data]
    print(tabulate(table_data, headers=report_data.headers, showindex=True))