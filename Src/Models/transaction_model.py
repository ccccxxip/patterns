import datetime
from Src.Core.base_model import base_model
from Src.Models.warehouse_model import warehouse_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model
from Src.Core.validator import validator
from Src.Core.exception import arguments_exception
from Src.Core.common import common


class transaction_model(base_model):
    """
    Модель складской транзакции (движения номенклатуры)
    Описывает операции поступления и расхода товаров на складе
    """

    def __init__(self):
        super().__init__()
        self.__warehouse: warehouse_model = None
        self.__nomenclature: nomenclature_model = None
        self.__unit: unit_model = None
        self.__value: float = 0.0
        self.__period: datetime.datetime = datetime.datetime.now()

    @property
    def warehouse(self) -> warehouse_model:
        """Склад проведения транзакции"""
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
        """Единица измерения движения"""
        return self.__unit

    @unit.setter
    def unit(self, value: unit_model):
        validator.validate(value, unit_model, field_name="unit")
        self.__unit = value

    @property
    def value(self) -> float:
        """Количество: приход (+), расход (-)"""
        return self.__value

    @value.setter
    def value(self, source: float):
        validator.validate(source, (int, float), field_name="value")
        val = float(source)
        if val == 0:
            raise arguments_exception("value", "Значение транзакции не может быть равно 0")
        self.__value = val

    @property
    def period(self) -> datetime.datetime:
        """Дата и время проведения транзакции"""
        return self.__period

    @period.setter
    def period(self, value: datetime.datetime):
        validator.validate(value, datetime.datetime, field_name="period")
        self.__period = value

    def __str__(self) -> str:
        """Представление транзакции для логирования"""
        nom_name = self.__nomenclature.name if self.__nomenclature is not None else ""
        return f"{nom_name}, количество: {self.__value}"

    @property
    def storage(self) -> warehouse_model:
        """Алиас для warehouse"""
        return self.__warehouse

    @storage.setter
    def storage(self, value: warehouse_model):
        self.warehouse = value

    @property
    def range(self) -> unit_model:
        """Алиас для unit"""
        return self.__unit

    @range.setter
    def range(self, value: unit_model):
        self.unit = value

    @classmethod
    def create_transaction(cls, warehouse: warehouse_model, nomenclature: nomenclature_model, unit: unit_model,
                           value: float, period: datetime.datetime = None) -> "transaction_model":
        """Базовый фабричный метод создания транзакции с валидацией"""
        t = cls()
        t.warehouse = warehouse
        t.nomenclature = nomenclature
        t.unit = unit
        t.value = float(value)
        if period is not None:
            t.period = period
        return t

    @classmethod
    def create_receipt(cls, warehouse: warehouse_model, nomenclature: nomenclature_model, unit: unit_model,
                       value: float, period: datetime.datetime = None) -> "transaction_model":
        """Фабричный метод создания транзакции поступления"""
        return cls.create_transaction(warehouse, nomenclature, unit, abs(float(value)), period)

    @classmethod
    def create_expense(cls, warehouse: warehouse_model, nomenclature: nomenclature_model, unit: unit_model,
                       value: float, period: datetime.datetime = None) -> "transaction_model":
        """Фабричный метод создания транзакции списания"""
        return cls.create_transaction(warehouse, nomenclature, unit, -abs(float(value)), period)

    @classmethod
    def create(cls, data: dict) -> "transaction_model":
        """
        Фабричный метод создания модели транзакции через рефлексию
        """
        if not isinstance(data, dict):
            return cls()

        item = cls()
        for field in common.get_fields(item):
            if field in data and data[field] is not None:
                setattr(item, field, data[field])

        return item
