from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class ReportData(Generic[T]):
    """Базовая модель для хранения данных отчёта с заголовками и данными."""

    headers: list[str]
    data: list[T]

@dataclass
class ReportAvgData:
    """Модель данных для отчёта среднего времени ответа по обработчикам."""

    handler: str
    request_count: int
    response_time: float

@dataclass
class CalculatedAvgField:
    """Вспомогательная модель для вычисления среднего времени ответа."""

    request_count: int = field(default=1)
    response_time: list[float] = field(default_factory=list)

    @property
    def avg_response_time(self) -> float:
        """Вычисляет среднее время ответа на основе собранных данных."""

        return round(sum(self.response_time) / self.request_count, 3)


@dataclass
class FilterParam:
    """Модель параметров для фильтрации данных отчёта."""

    date: str = field(default=None)