from abc import ABC, abstractmethod
from Src.Core.abstract_convertor import abstract_convertor


class abstract_convert_factory(ABC):
    """
    Абстрактная фабрика конвертеров данных
    Определяет интерфейс создания конвертеров и преобразования данных
    """

    @abstractmethod
    def create(self, source_or_type: object) -> abstract_convertor:
        """
        Фабричный метод: подбор конвертера по типу, объекту или ключу
        """
        pass

    @abstractmethod
    def Convert(self, item: object) -> object:
        """
        Преобразование переданного объекта в структуру словарей
        """
        pass
