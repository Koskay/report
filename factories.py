from reports.collectors import AvgResponseTimeCollector
from reports.builders import ReportBuilder

from utils.readers import FileLineGenerator


def create_report_builder(report_type: str) -> ReportBuilder:
    """Создает построитель отчётов в зависимости от типа отчёта."""
    match report_type:
        case "average":
            return ReportBuilder(
                file_reader=FileLineGenerator(),
                collector_report_data=AvgResponseTimeCollector(),
            )
        case _:
            raise ValueError(f"Не известный тип отчета: {report_type}")