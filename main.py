import argparse
import os
from dataclasses import dataclass

from factories import create_report_builder
from reports.collectors import ReportData
from reports.models import FilterParam
from reports.outputs import display_to_console

@dataclass
class ReportRequest:
    """Модель запроса на создание отчёта."""
    file_paths: list[str]
    report_name: str
    filters: FilterParam

def args_parser() -> ReportRequest:
    """Парсит аргументы командной строки и возвращает параметры запроса."""
    parser = argparse.ArgumentParser(description="Обработать файл журнала и сформировать отчет.")
    parser.add_argument("--file", nargs="+", help="Список файлов для обработки", required=True)
    parser.add_argument("--report", choices=["average", "sum", "count"], help="Типы отчетов", required=True)
    parser.add_argument("--date", help="Фильтрация по дате", default=None)

    args = parser.parse_args()
    valid_path = all(os.path.exists(file_path) for file_path in args.file)
    if not valid_path:
        raise FileNotFoundError("Файл(ы) по указанному пути не найден")

    filters = FilterParam(date=args.date)

    return ReportRequest(file_paths=args.file, report_name=args.report, filters=filters)


def create_report_from_file(params: ReportRequest) -> ReportData:
    """Создает отчёт на основе переданных параметров."""
    builder = create_report_builder(params.report_name)
    report_data = builder.build(file_paths=params.file_paths, filters=params.filters)
    return report_data


def main():
    """Главная функция программы."""
    args = args_parser()
    report_data = create_report_from_file(args)
    display_to_console(report_data=report_data)


if __name__ == "__main__":
    main()