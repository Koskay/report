import pytest

from main import args_parser, ReportRequest


def test_valid_args_parser_returns(monkeypatch):
    """Проверяет, что парсер аргументов корректно обрабатывает валидные параметры командной строки."""
    monkeypatch.setattr(
        "sys.argv",
        ["script.py", "--file", "example1.log", "--report", "average"],
    )

    result = args_parser()

    assert isinstance(result, ReportRequest)
    assert result.file_paths == ["example1.log"]
    assert result.report_name == "average"


def test_invalid_args_parser_returns(monkeypatch):
    """Проверяет, что парсер аргументов завершает программу при получении неизвестных аргументов."""
    monkeypatch.setattr(
        "sys.argv",
        ["script.py", "--invalid", "example1.log", "--report", "average"],
    )
    with pytest.raises(SystemExit):
        args_parser()


def test_invalid_file_path_in_args(monkeypatch):
    """Проверяет, что парсер аргументов выбрасывает исключение при указании несуществующего файла."""
    invalid_path = "/nonexistent/path/to/file.log"
    monkeypatch.setattr(
        "sys.argv",
        ["script.py", "--file", invalid_path, "--report", "average"],
    )
    with pytest.raises(FileNotFoundError):
        args_parser()
