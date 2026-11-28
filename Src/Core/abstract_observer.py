from abc import ABC, abstractmethod


class abstract_observer(ABC):
    """
    Абстрактный базовый класс наблюдателя
    Определяет контракт обработки событий
    """

    @abstractmethod
    def handler(self, event_types: str, params: object = None) -> None:
        """
        Выполнить обработку события
        """
        pass
