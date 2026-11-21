from collections import defaultdict
from typing import List
from Src.Models.osv_row_model import osv_row_model
from Src.Logics.storage_manager import storage_manager
from Src.Logics.prototype import prototype
from Src.Dtos.filter_dto import filter_dto


class osv_service:
    """
    Сервис формирования оборотно-сальдовой ведомости (ОСВ)
    Формирует строки ведомости на основе складских транзакций
    и применяет шаблон «Прототип» для фильтрации данных
    """

    def __init__(self, storage: storage_manager = None):
        self.__storage = storage or storage_manager()

    def get_base_rows(self) -> List[osv_row_model]:
        """
        Формирует строки ОСВ путем агрегации складских транзакций по номенклатуре
        Использует хэш-индексацию
        """
        warehouses = self.__storage.get_entities_by_type("warehouse")
        default_wh = warehouses[0]
        nomenclatures = self.__storage.get_entities_by_type("nomenclature")
        transactions = self.__storage.get_entities_by_type("transaction")

        turnovers_in = defaultdict(float)
        turnovers_out = defaultdict(float)

        for t in transactions:
            turnovers_in[t.nomenclature.id] += max(0.0, t.value)
            turnovers_out[t.nomenclature.id] += max(0.0, -t.value)

        return [
            osv_row_model.create_row(default_wh, nom, nom.unit, 50.0, turnovers_in[nom.id], turnovers_out[nom.id])
            for nom in nomenclatures
        ]

    def build(self, filter_: filter_dto = None) -> List[osv_row_model]:
        """
        Формирует ОСВ с применением шаблона «Прототип» для фильтрации
        """
        return prototype(self.get_base_rows()).clone(filter_).data