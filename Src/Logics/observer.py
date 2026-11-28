from typing import List
from Src.Core.abstract_observer import abstract_observer
from Src.Core.validator import validator


class observer:
    """
    Диспетчер событий
    Регистрирует наблюдателей и рассылает уведомления о возникших событиях
    """

    # Список зарегистрированных наблюдателей
    handlers: List[abstract_observer] = []

    @staticmethod
    def add(source: abstract_observer) -> None:
        """
        Добавить объект под наблюдение
        """
        validator.validate(source, abstract_observer)

        for handler in observer.handlers:
            if handler == source:
                return

        observer.handlers.append(source)

    @staticmethod
    def delete(source: abstract_observer) -> None:
        """
        Удалить объект из-под наблюдения
        """
        validator.validate(source, abstract_observer)

        observer.handlers = [h for h in observer.handlers if h != source]

    @staticmethod
    def create(event_types: str, params: object = None) -> None:
        """
        Оповестить всех наблюдателей о событии
        """
        for handler in observer.handlers:
            handler.handler(event_types, params)

    @staticmethod
    def clear() -> None:
        """
        Очистить список наблюдателей
        """
        observer.handlers.clear()
