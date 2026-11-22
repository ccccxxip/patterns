from collections import defaultdict
from typing import List, Optional, Tuple, Set
from datetime import datetime
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

    def _filter_by_entities(self, nomenclatures: list, transactions: list, f: filter_dto) -> Tuple[list, list]:
        """Фильтрация номенклатуры и транзакций по критериям сущностей через Прототип"""
        if not (f.name or f.id or f.filters):
            return nomenclatures, transactions

        target_noms = prototype(nomenclatures).clone(f).data
        target_nom_ids = {n.id for n in target_noms}
        matched_txs = [t for t in transactions if t.nomenclature.id in target_nom_ids]
        return target_noms, matched_txs

    def _calculate_start_balances(self, proto: prototype, start_period: Optional[datetime]) -> Tuple[defaultdict, Set[int]]:
        """Расчет начальных остатков до даты начала периода через Прототип"""
        start_balances = defaultdict(float)
        before_tx_ids = set()

        if start_period is not None:
            before_filter = filter_dto()
            before_filter.end_period = start_period
            before_txs = proto.clone(before_filter).data
            for t in before_txs:
                start_balances[t.nomenclature.id] += t.value
                before_tx_ids.add(id(t))

        return start_balances, before_tx_ids

    def _calculate_turnovers(
        self,
        proto: prototype,
        start_period: Optional[datetime],
        end_period: Optional[datetime],
        exclude_tx_ids: Set[int]
    ) -> Tuple[defaultdict, defaultdict]:
        """Расчет приходных и расходных оборотов за указанный период через Прототип"""
        turnovers_in = defaultdict(float)
        turnovers_out = defaultdict(float)

        period_filter = filter_dto()
        period_filter.start_period = start_period
        period_filter.end_period = end_period
        period_txs = proto.clone(period_filter).data

        for t in period_txs:
            if id(t) not in exclude_tx_ids:
                turnovers_in[t.nomenclature.id] += max(0.0, t.value)
                turnovers_out[t.nomenclature.id] += max(0.0, -t.value)

        return turnovers_in, turnovers_out

    def build(self, filter_: Optional[filter_dto] = None) -> List[osv_row_model]:
        """
        Формирует ОСВ по алгоритму расчета сальдо
        """
        f = filter_ or filter_dto()

        warehouses = self.__storage.get_entities_by_type("warehouse")
        default_wh = warehouses[0]
        nomenclatures = self.__storage.get_entities_by_type("nomenclature")
        transactions = self.__storage.get_entities_by_type("transaction")

        # Фильтрация данных по критериям сущностей через Прототип
        target_noms, matched_txs = self._filter_by_entities(nomenclatures, transactions, f)
        proto = prototype(matched_txs)

        # Фильтр по дате начала и расчет начальных остатков
        start_balances, before_ids = self._calculate_start_balances(proto, f.start_period)

        # Фильтр по датам и расчет оборотов
        turnovers_in, turnovers_out = self._calculate_turnovers(proto, f.start_period, f.end_period, before_ids)

        # Объединение записей и расчет конечных остатков в osv_row_model
        return [
            osv_row_model.create_row(
                warehouse=default_wh,
                nomenclature=nom,
                unit=nom.unit,
                start_balance=round(start_balances[nom.id], 4),
                turnover_in=round(turnovers_in[nom.id], 4),
                turnover_out=round(turnovers_out[nom.id], 4)
            )
            for nom in target_noms
        ]
