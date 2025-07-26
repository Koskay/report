import os
from typing import Generator


class FileLineGenerator:
    """Читает файлы построчно, возвращая генераторы строк."""

    def get_line_generator_list(self, file_paths: list[str]) -> list[Generator[str, None, None]]:
        """Возвращает список генераторов строк для каждого файла."""
        return [self._get_line(path) for path in file_paths]

    def _get_line(self, file_path: str) -> Generator[str, None, None]:
        """Генератор, который читает файл построчно. Бросает ValueError, если файл пуст."""
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"Файл {file_path} пуст!")

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                yield line