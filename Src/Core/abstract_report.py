from Src.Dtos.report_result_dto import report_result_dto
from abc import ABC, abstractmethod
from Src.Core.base_model import base_model

"""абстрактный класс для формирования результата"""
class abstract_report():

    """сформировать отчет"""
    @abstractmethod
    def build(self, source:base_model) -> report_result_dto:
        pass