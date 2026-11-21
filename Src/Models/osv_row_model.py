from Src.Core.base_model import base_model
from Src.Models.warehouse_model import warehouse_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model
from Src.Core.validator import validator
from Src.Core.common import common


class osv_row_model(base_model):
    """
    Модель строки оборотно-сальдовой ведомости 
    Хранит информацию об остатках и оборотах номенклатуры по складу за период
    """

    def __init__(self):
        super().__init__()
        self.__warehouse: warehouse_model = None
        self.__nomenclature: nomenclature_model = None
        self.__unit: unit_model = None
        self.__start_balance: float = 0.0
        self.__turnover_in: float = 0.0
        self.__turnover_out: float = 0.0
        self.__end_balance: float = 0.0

    @property
    def warehouse(self) -> warehouse_model:
        """Склад хранения"""
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse_model):
        validator.validate(value, warehouse_model, field_name="warehouse")
        self.__warehouse = value

    @property
    def nomenclature(self) -> nomenclature_model:
        """Номенклатурная позиция"""
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model, field_name="nomenclature")
        self.__nomenclature = value

    @property
    def unit(self) -> unit_model:
        """Единица измерения"""
        return self.__unit

    @unit.setter
    def unit(self, value: unit_model):
        validator.validate(value, unit_model, field_name="unit")
        self.__unit = value

    @property
    def start_balance(self) -> float:
        """Начальный остаток на складе"""
        return self.__start_balance

    @start_balance.setter
    def start_balance(self, value: float):
        validator.validate(value, (int, float), field_name="start_balance")
        self.__start_balance = float(value)
        self._recalc_end_balance()

    @property
    def turnover_in(self) -> float:
        """Приход (оборот поступления) за период"""
        return self.__turnover_in

    @turnover_in.setter
    def turnover_in(self, value: float):
        validator.validate(value, (int, float), field_name="turnover_in")
        self.__turnover_in = float(value)
        self._recalc_end_balance()

    @property
    def turnover_out(self) -> float:
        """Расход (оборот списания) за период"""
        return self.__turnover_out

    @turnover_out.setter
    def turnover_out(self, value: float):
        validator.validate(value, (int, float), field_name="turnover_out")
        self.__turnover_out = float(value)
        self._recalc_end_balance()

    @property
    def end_balance(self) -> float:
        """Конечный остаток на складе"""
        return self.__end_balance

    @end_balance.setter
    def end_balance(self, value: float):
        validator.validate(value, (int, float), field_name="end_balance")
        self.__end_balance = float(value)

    def _recalc_end_balance(self):
        """Перерасчет конечного остатка: начальный + приход - расход"""
        self.__end_balance = round(self.__start_balance + self.__turnover_in - self.__turnover_out, 4)

    @classmethod
    def create_row(cls, warehouse: warehouse_model, nomenclature: nomenclature_model, unit: unit_model,
                   start_balance: float = 0.0, turnover_in: float = 0.0, turnover_out: float = 0.0) -> "osv_row_model":
        """Именованный фабричный метод создания строки ОСВ """
        row = cls()
        row.warehouse = warehouse
        row.nomenclature = nomenclature
        row.unit = unit
        row.start_balance = start_balance
        row.turnover_in = turnover_in
        row.turnover_out = turnover_out
        return row

    @classmethod
    def create(cls, data: dict) -> "osv_row_model":
        """
        Фабричный метод создания строки ОСВ через рефлексию
        """
        if not isinstance(data, dict):
            return cls()

        item = cls()
        for field in common.get_fields(item):
            if field in data and data[field] is not None:
                setattr(item, field, data[field])

        return item
