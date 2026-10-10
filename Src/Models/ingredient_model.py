from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model


class ingredient_model(base_model):
    """
    Доменная модель: Строка технологической карты (Ингредиент)
    Хранит веса Брутто и Нетто для конкретной номенклатуры
    """

    def __init__(self, nomenclature: nomenclature_model, net_weight: float, gross_weight: float, unit: unit_model) -> None:
        """
        Инициализирует ингредиент

        nomenclature: Номенклатура (продукт, полуфабрикат или упаковка)
        net_weight: Вес Нетто (без отходов)
        gross_weight: Вес Брутто (с отходами)
        unit: Единица измерения, в которой указаны веса
        """
        super().__init__()
        self.nomenclature = nomenclature
        self.name = nomenclature.name
        self.net_weight = net_weight
        self.gross_weight = gross_weight
        self.unit = unit

    @property
    def nomenclature(self) -> nomenclature_model:
        """Возвращает номенклатуру ингредиента"""
        return self._nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model) -> None:
        """Задаёт номенклатуру ингредиента"""
        if not isinstance(value, nomenclature_model):
            raise arguments_exception("nomenclature", "Номенклатура должна быть объектом nomenclature_model")

        self._nomenclature = value

    @property
    def unit(self) -> unit_model:
        """Возвращает единицу измерения весов"""
        return self._unit

    @unit.setter
    def unit(self, value: unit_model) -> None:
        """Задаёт единицу измерения весов"""
        if not isinstance(value, unit_model):
            raise arguments_exception("unit", "Единица измерения должна быть объектом unit_model")

        self._unit = value

    @property
    def net_weight(self) -> float:
        """Возвращает вес Нетто"""
        return self._net_weight

    @net_weight.setter
    def net_weight(self, value: float) -> None:
        """
        Задаёт вес Нетто

        raises arguments_exception: Если передано не число или отрицательное число
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise arguments_exception("net_weight", "Вес Нетто должен быть числом")

        if value < 0:
            raise arguments_exception("net_weight", "Вес Нетто не может быть отрицательным")

        self._net_weight = float(value)

    @property
    def gross_weight(self) -> float:
        """Возвращает вес Брутто"""
        return self._gross_weight

    @gross_weight.setter
    def gross_weight(self, value: float) -> None:
        """
        Задаёт вес Брутто

        raises arguments_exception: Если передано не число или отрицательное число
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise arguments_exception("gross_weight", "Вес Брутто должен быть числом")

        if value < 0:
            raise arguments_exception("gross_weight", "Вес Брутто не может быть отрицательным")

        self._gross_weight = float(value)

    @staticmethod
    def create(nomenclature: nomenclature_model, net_quantity: float, gross_quantity: float) -> "ingredient_model":
        """
        Фабричный метод: ингредиент по количеству в единице измерения номенклатуры

        Количество переводится в базовую единицу через unit.to_base()

        nomenclature: Номенклатура
        net_quantity: Нетто в единице номенклатуры
        gross_quantity: Брутто в единице номенклатуры
        """
        if not isinstance(nomenclature, nomenclature_model):
            raise arguments_exception("nomenclature", "Номенклатура должна быть объектом nomenclature_model")

        unit = nomenclature.unit
        return ingredient_model(
            nomenclature,
            unit.to_base(net_quantity),
            unit.to_base(gross_quantity),
            unit.base_unit,
        )