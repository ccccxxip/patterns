from abc import ABC, abstractmethod
from typing import Type, Callable
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model


class abstract_report(ABC):
    """Абстрактный базовый класс для формирования отчётов"""

    def __init__(self):
        self.__handlers: dict[Type, Callable] = {}

    @property
    @abstractmethod
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта"""
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Расширение файла отчёта"""
        pass

    @property
    @abstractmethod
    def is_attachment(self) -> bool:
        """Флаг скачивания вложения"""
        pass

    def register(self, entity_type: Type, handler: Callable) -> None:
        """
        Связка конкретного типа с внутренним методом
        Позволяет масштабировать генератор отчётов для новых составных сущностей без изменения общего кода
        """
        self.__handlers[entity_type] = handler

    def build(self, source: base_model) -> report_result_dto:
        """
        Сформировать отчёт для переданной сущности.
        Ищет специализированный обработчик в реестре, иначе вызывает универсальный генератор.
        """
        handler = self.__handlers.get(source.__class__)
        if handler is not None:
            return handler(source)
        return self._build_generic(source)

    @abstractmethod
    def _build_generic(self, source: base_model) -> report_result_dto:
        """Универсальное построение отчёта для одиночной сущности через рефлексию"""
        pass

    def _format_value(self, val, source=None) -> str:
        """Универсальное форматирование значения поля для отчётов"""
        if val is None or val == "":
            return ""
        if isinstance(val, base_model):
            return "базовая" if source is not None and val is source else val.name
        if isinstance(val, float):
            return f"{val:.2f}"
        if hasattr(val, "name"):
            return str(val.name)
        return str(val)
