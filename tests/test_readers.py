import pytest
from utils.readers import FileLineGenerator


@pytest.fixture
def generator():
    return FileLineGenerator()


def test_reading_non_empty_file(tmp_path, generator):
    """Проверяет, что генератор строк корректно читает непустой файл и возвращает все строки."""
    p = tmp_path / "test.log"
    content = ["first\n", "second\n", "third\n"]
    p.write_text("".join(content), encoding="utf-8")

    gens = generator.get_line_generator_list([str(p)])
    assert len(gens) == 1

    lines = list(gens[0])
    assert lines == content


def test_empty_file_raises_value_error(tmp_path, generator):
    """Проверяет, что при попытке чтения пустого файла генератор выбрасывает ValueError."""
    p = tmp_path / "empty.log"
    p.write_text("", encoding="utf-8")

    gen = generator._get_line(str(p))
    with pytest.raises(ValueError):
        next(gen)