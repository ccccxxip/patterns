from abc import ABC, abstractmethod


class abstract_prototype(ABC):
    """
    Абстрактный базовый класс шаблона проектирования «Прототип»
    Определяет контракт клонирования данных с применением фильтрации
    """

    @abstractmethod
    def clone(self, filter_: object = None) -> "abstract_prototype":
        """
        Клонировать данные с опциональным применением фильтра
        """
        pass
