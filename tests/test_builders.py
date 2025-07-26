import pytest
import json
from unittest.mock import Mock

from reports.builders import ReportBuilder
from reports.models import ReportData

@pytest.fixture
def report_data():
    return ReportData(headers=['foo'], data=["data", "data2"])

@pytest.fixture
def collector_mock():
    mock = Mock()
    return mock

@pytest.fixture
def file_reader_mock():
    mock = Mock()
    return mock

@pytest.fixture
def filter_mock():
    mock = Mock()
    return mock

@pytest.fixture
def builder(file_reader_mock, collector_mock):
    return ReportBuilder(
        file_reader=file_reader_mock,
        collector_report_data=collector_mock
    )


import json
from unittest.mock import Mock


def test_build_invokes_dependencies_and_returns_report(builder, file_reader_mock, collector_mock, report_data):
    """Проверяет полный процесс сборки отчёта: чтение файлов, обработку строк и возврат итогового отчёта."""
    lines = ['{"url": "/a", "time": 1}', '{"url": "/b", "time": 2}']
    file_reader_mock.get_line_generator_list.return_value = [iter(lines)]
    collector_mock.get_collected_data.return_value = report_data

    builder._process_line = Mock()
    result = builder.build(['file.log'])

    file_reader_mock.get_line_generator_list.assert_called_once_with(file_paths=['file.log'])
    collector_mock.get_collected_data.assert_called_once()
    assert result == report_data


def test_process_line_parses_json_and_calls_collect(builder, collector_mock):
    """Проверяет, что метод _process_line корректно парсит JSON и передаёт данные в коллектор."""
    line = json.dumps({'key': 'value'})
    builder._process_line(line)
    collector_mock.collect_data.assert_called_once_with({'key': 'value'})


def test_process_line_with_filter(builder, filter_mock, collector_mock):
    """Проверяет, что метод _process_line правильно применяет фильтр перед сбором данных."""
    line = {'@timestep': 'value'}
    json_line = json.dumps(line)
    filter_mock.matches.return_value = True
    builder._process_line(json_line, filter_mock)

    filter_mock.matches.assert_called_once_with(line)
    collector_mock.collect_data.assert_called_once_with(line)