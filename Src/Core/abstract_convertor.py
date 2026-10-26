from abc import ABC, abstractmethod


class abstract_convertor(ABC):
    """
    Абстрактный базовый класс для всех конвертеров данных
    Обеспечивает преобразование любых объектов в словарь {поле: значение}
    """

    def __init__(self, factory=None):
        """
        Инициализация конвертера с возможностью передачи фабрики
        """
        self._factory = factory

    @property
    def factory(self):
        """Ссылка на абстрактную фабрику конвертеров"""
        return self._factory

    @factory.setter
    def factory(self, value):
        self._factory = value

    @abstractmethod
    def Convert(self, item: object, field_name: str = None) -> dict:
        """
        Абстрактный метод преобразования переданного объекта в словарь

        item: object
            Любой объект или значение для конвертации

        field_name: str, optional
            Наименование поля (актуально для скалярных типов, по дефолту "value")

        returns: dict
            Словарь вида {наименование_поля: значение}
        """
        pass
