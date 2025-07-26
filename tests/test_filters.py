import pytest
from utils.filters import DateFilter, FilterParam

class TestDateFilter:
    def test_init_with_valid_date(self):
        """Проверяет, что фильтр корректно инициализируется с валидной датой и находит совпадения."""
        fp = FilterParam(date="2025-26-07")
        df = DateFilter(filter_param=fp)
        matches = df.matches({"@timestamp": "2025-07-26T13:57:32+00:00"})
        assert matches is True

    @pytest.mark.parametrize("bad_date", ["07-26-2025", "2025/26/07", "20252607"])
    def test_init_with_invalid_date_raises(self, bad_date):
        """Проверяет, что фильтр выбрасывает исключение при неправильном формате даты."""
        fp = FilterParam(date=bad_date)
        with pytest.raises(ValueError) as exc:
            DateFilter(filter_param=fp)
        assert "Дата для фильтра должна быть в формате %Y-%d-%m" in str(exc.value)

    def test_matches_false_when_different_date(self):
        """Проверяет, что фильтр возвращает False при несовпадении дат."""
        fp = FilterParam(date="2021-01-01")
        df = DateFilter(filter_param=fp)

        ts = "2021-01-02T00:00:00"
        line = {"@timestamp": ts}
        assert df.matches(line) is False

    def test_matches_raises_on_missing_key(self):
        """Проверяет, что фильтр выбрасывает исключение при отсутствии ключа @timestamp."""
        fp = FilterParam(date="2021-01-01")
        df = DateFilter(filter_param=fp)

        with pytest.raises(ValueError) as exc:
            df.matches({"no_timestamp": "2021-01-01T00:00:00"})
        assert "Ключ для даты должен быть @timestamp." in str(exc.value)

    @pytest.mark.parametrize("bad_ts", ["not-a-date", "2021-13-01T00:00:00", ""])
    def test_matches_raises_on_invalid_iso(self, bad_ts):
        """Проверяет, что фильтр выбрасывает исключение при некорректном ISO формате времени."""
        fp = FilterParam(date="2021-01-01")
        df = DateFilter(filter_param=fp)
        with pytest.raises(ValueError):
            df.matches({"@timestamp": bad_ts})