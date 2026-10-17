from Src.Core.abstract_report import abstract_report
from abc import ABC, abstractmethod
from Src.Dtos.report_type_dto import report_type_enum

"""абстрактная фабрика отчетов"""
class abstract_factory(ABC):
    
    """подобрать нужный класс отчета"""
    @abstractmethod
    def create(self, report_type: report_type_enum) -> abstract_report:
        pass