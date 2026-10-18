from abc import ABC, abstractmethod
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model


class abstract_report(ABC):
    """Абстрактный базовый класс для формирования отчётов"""

    @property
    @abstractmethod
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта (например, text/html, application/xml, text/csv)"""
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Расширение файла отчёта (например, csv, md, html, xml, txt)"""
        pass

    @property
    @abstractmethod
    def is_attachment(self) -> bool:
        """Флаг: отдавать ли отчёт как скачиваемый файл (attachment) или как текст"""
        pass

    @abstractmethod
    def build(self, source: base_model) -> report_result_dto:
        """Сформировать отчёт для переданной сущности"""
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
