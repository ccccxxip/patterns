from abc import ABC, abstractmethod
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_type_dto import report_type_enum


class abstract_factory(ABC):
    """Абстрактная фабрика отчётов"""

    @abstractmethod
    def create(self, report_type: report_type_enum) -> abstract_report:
        """Подобрать нужный класс отчёта по типу"""
        pass

    @abstractmethod
    def create_default(self) -> abstract_report:
        """Подобрать класс отчёта по умолчанию из настроек"""
        pass
