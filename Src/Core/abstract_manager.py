from abc import ABC


class abstract_manager(ABC):
    """Абстрактный класс для реализации загрузки и обработки данных"""

    _file_name: str = ""
    _is_loaded: bool = False
    _data: list = []

    def load(self, file_name: str = "") -> None:
        """Загружает данные из источника (реализуется в наследниках)"""
        pass

    def convert(self) -> bool:
        """Преобразует загруженные данные в доменную модель (реализуется в наследниках)"""
        return False

    @property
    def is_loaded(self) -> bool:
        """Возвращает признак успешной загрузки и обработки данных"""
        return self._is_loaded