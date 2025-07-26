from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass

from reports.models import FilterParam


class BaseFilter(ABC):

    @abstractmethod
    def matches(self, line: dict) -> bool:
        """Проверяет, соответствует ли строка лога условиям фильтра."""
        pass


# Пример конкретного фильтра: фильтрация по дате
@dataclass
class DateFilter(BaseFilter):
    filter_param: FilterParam

    def __post_init__(self):
        """Валидирует формат даты при инициализации фильтра."""
        try:
            datetime.strptime(self.filter_param.date, "%Y-%d-%m")
        except ValueError:
            raise ValueError(f"Дата для фильтра должна быть в формате %Y-%d-%m")

    def matches(self, line: dict) -> bool:
        """Проверяет, соответствует ли дата в строке лога заданной дате фильтра."""
        try:
            dt = datetime.fromisoformat(line['@timestamp'])
            formatted_date = dt.strftime("%Y-%d-%m")
            if formatted_date == self.filter_param.date:
                return True
            return False
        except KeyError:
            raise ValueError("Ключ для даты должен быть @timestamp.")


def filter_factory(filter_param: FilterParam) -> BaseFilter | None:
    """Создает соответствующий фильтр на основе переданных параметров."""
    if filter_param.date:
        return DateFilter(filter_param=filter_param)
    return None