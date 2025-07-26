import json
from dataclasses import dataclass
from itertools import zip_longest
from reports.collectors import BaseCollector
from reports.models import ReportData, FilterParam
from utils.filters import BaseFilter, filter_factory
from utils.readers import FileLineGenerator


@dataclass
class ReportBuilder:
    """Строитель отчётов, координирующий чтение файлов, фильтрацию и сбор данных."""

    file_reader: FileLineGenerator
    collector_report_data: BaseCollector

    def build(self, file_paths: list[str], filters: FilterParam | None = None) -> ReportData:
        """Строит отчёт на основе указанных файлов с применением фильтров при необходимости."""

        filter_obj = filter_factory(filters) if filters else None

        file_generators = self.file_reader.get_line_generator_list(file_paths=file_paths)
        for lines in zip_longest(*file_generators, fillvalue=None):
            for line in lines:
                if line is None:
                    continue
                self._process_line(line, filter_obj=filter_obj)
        return self.collector_report_data.get_collected_data()


    def _process_line(self, line: str, filter_obj: BaseFilter | None = None) -> None:
        """Обрабатывает одну строку лога: парсит JSON и передаёт данные в коллектор при прохождении фильтра."""

        log = json.loads(line)
        if filter_obj is None or filter_obj.matches(log):
            self.collector_report_data.collect_data(log)