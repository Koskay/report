from abc import ABC, abstractmethod

from reports.models import ReportData, CalculatedAvgField, ReportAvgData


class BaseCollector(ABC):

    @abstractmethod
    def collect_data(self, line: dict) -> None:
        ...

    def get_collected_data(self):
        ...


class AvgResponseTimeCollector(BaseCollector):
    """Сборщик данных для отчёта среднего времени ответа по URL-обработчикам."""

    def __init__(self):
        self._report_avg_data = dict()

    def collect_data(self, line: dict) -> None:
        """Собирает данные из строки лога, проверяя её валидность и обновляя статистику."""

        if not self._validate_line(line):
            raise ValueError("Invalid log line format for avg report")

        self._collect_handler_data(line)
        self._update_response_times(line)

    @staticmethod
    def _validate_line(line: dict) -> bool:
        """Проверяет, содержит ли строка лога все необходимые поля для отчёта."""

        required_fields = {'url', 'response_time'}
        return all(field in line for field in required_fields)

    def _collect_handler_data(self, line: dict) -> None:
        """Инициализирует или обновляет счётчик запросов для URL-обработчика."""

        url = line['url']

        if url not in self._report_avg_data.keys():
            self._report_avg_data[url] = CalculatedAvgField()
        else:
            self._report_avg_data[url].request_count += 1

    def _update_response_times(self, line: dict) -> None:
        """Добавляет время ответа к списку времен для соответствующего URL-обработчика."""

        self._report_avg_data[line["url"]].response_time.append(line['response_time'])

    def get_collected_data(self) -> ReportData:
        """Возвращает финальный отчёт с агрегированными данными по среднему времени ответа."""

        avg_data = [ReportAvgData(
            handler=key,
            request_count=value.request_count,
            response_time=value.avg_response_time
        ) for key, value in self._report_avg_data.items()]

        return ReportData(headers=["url", "count", "avg_response_time"], data=avg_data)


class UserAgentCollector(BaseCollector):

    def collect_data(self, line: dict) -> None:
        pass

    def get_collected_data(self):
        pass