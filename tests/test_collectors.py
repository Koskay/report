import pytest

from reports.collectors import AvgResponseTimeCollector, ReportData, ReportAvgData, CalculatedAvgField


@pytest.fixture
def collector():
    return AvgResponseTimeCollector()

@pytest.fixture
def file_data():
    return [
        {'url': '/test', 'response_time': 0.132},
        {'url': '/test', 'response_time': 0.333},
        {'url': '/test2', 'response_time': 0.121},
        {'url': '/test2', 'response_time': 0.321},
        {'url': '/test2', 'response_time': 0.111},
        {'url': '/test3', 'response_time': 0.311},
    ]


class TestAvgCollector:
    def test_validate_line_pass(self, collector):
        """Проверяет, что валидация строки проходит успешно при наличии обязательных полей."""
        assert collector._validate_line({'url': '/home', 'response_time': 100}) is True

    def test_validate_line_fail(self, collector):
        """Проверяет, что валидация строки завершается неудачей при отсутствии обязательных полей."""
        assert collector._validate_line({'url': '/home'}) is False
        assert collector._validate_line({'response_time': 50}) is False

    def test_collect_data_invalid_line_raises(self, collector):
        """Проверяет, что коллектор выбрасывает исключение при попытке обработки невалидной строки."""
        with pytest.raises(ValueError):
            collector.collect_data({'url': '/test'})

    def test_single_line_collection(self, collector):
        """Проверяет корректность сбора данных для одной строки."""
        line = {'url': '/api', 'response_time': 0.111}
        collector.collect_data(line)
        report = collector.get_collected_data()

        assert report.headers == ["url", "count", "avg_response_time"]

        assert isinstance(report, ReportData)
        assert len(report.data) == 1
        item = report.data[0]
        assert isinstance(item, ReportAvgData)
        assert item.handler == '/api'
        assert item.request_count == 1
        assert item.response_time == float(0.111)

    def test_multiple_lines_collection(self, collector, file_data):
        """Проверяет корректность агрегации данных при обработке нескольких строк."""
        for line in file_data:
            collector.collect_data(line)

        report = collector.get_collected_data()

        first_file_item = file_data[0]
        first_report_item = report.data[0]
        response_avg = round((file_data[0]["response_time"] + file_data[1]["response_time"]) / 2, 3)

        assert isinstance(report, ReportData)
        assert len(report.data) == 3
        assert first_report_item.handler == first_file_item['url']
        assert first_report_item.request_count == 2
        assert first_report_item.response_time == response_avg

    def test_internal_state_updated_after_data_collection(self, collector):
        """Проверяет, что внутреннее состояние коллектора корректно обновляется после сбора данных."""
        line = {'url': '/api', 'response_time': 0.111}
        collector._collect_handler_data(line)
        collector._update_response_times(line)
        assert "/api" in collector._report_avg_data.keys()
        assert isinstance(collector._report_avg_data["/api"], CalculatedAvgField)
        assert collector._report_avg_data["/api"].request_count == 1
        assert collector._report_avg_data["/api"].response_time == [float(0.111)]