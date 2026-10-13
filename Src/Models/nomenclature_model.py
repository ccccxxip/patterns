from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.constants import FULL_NAME_MAX_LENGTH
from Src.Core.nomenclature_type import nomenclature_type
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model


class nomenclature_model(base_model):
    """
    Модель данных "Номенклатура"
    Наследуется от base_model
    Включает в себя полное наименование, группу, единицу измерения и тип (продукт, полуфабрикат, упаковка)
    """

    def __init__(self, name: str, full_name: str, group: nomenclature_group_model, unit: unit_model,
                 nom_type: nomenclature_type = nomenclature_type.PRODUCT) -> None:
        """
        Инициализирует экземпляр модели номенклатуры

        name: Обычное наименование (до 50 символов, валидируется в base_model)
        full_name: Полное наименование (до 255 символов)
        group: Группа номенклатуры (экземпляр nomenclature_group_model)
        unit: Единица измерения (экземпляр unit_model)
        nom_type: Тип номенклатуры (по умолчанию продукт)
        """
        super().__init__()
        self.name = name
        self.full_name = full_name
        self.group = group
        self.unit = unit
        self.type = nom_type

    @property
    def full_name(self) -> str:
        """Возвращает полное наименование номенклатуры"""
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        """
        Задаёт полное наименование номенклатуры

        value: Непустая строка длиной до 255 символов
        raises arguments_exception: Если передана не строка, пустая строка или превышена длина 255 символов
        """
        if not isinstance(value, str):
            raise arguments_exception("full_name", "Полное наименование должно быть строкой")

        normalized_value = value.strip()

        if not normalized_value:
            raise arguments_exception("full_name", "Полное наименование не может быть пустым")

        if len(normalized_value) > FULL_NAME_MAX_LENGTH:
            raise arguments_exception(
                "full_name", f"Полное наименование не должно превышать {FULL_NAME_MAX_LENGTH} символов"
            )

        self._full_name = normalized_value

    @property
    def group(self) -> nomenclature_group_model:
        """Возвращает группу номенклатуры"""
        return self._group

    @group.setter
    def group(self, value: nomenclature_group_model) -> None:
        """Задаёт группу номенклатуры"""
        if not isinstance(value, nomenclature_group_model):
            raise arguments_exception("group", "Группа номенклатуры должна быть объектом nomenclature_group_model")

        self._group = value

    @property
    def unit(self) -> unit_model:
        """Возвращает единицу измерения номенклатуры"""
        return self._unit

    @unit.setter
    def unit(self, value: unit_model) -> None:
        """Задаёт единицу измерения номенклатуры"""
        if not isinstance(value, unit_model):
            raise arguments_exception("unit", "Единица измерения должна быть объектом unit_model")

        self._unit = value

    @property
    def type(self) -> nomenclature_type:
        """Возвращает тип номенклатуры (продукт, полуфабрикат, упаковка)"""
        return self._type

    @type.setter
    def type(self, value: nomenclature_type) -> None:
        """
        Задаёт тип номенклатуры

        raises arguments_exception: Если передан не nomenclature_type
        """
        if not isinstance(value, nomenclature_type):
            raise arguments_exception("type", "Тип номенклатуры должен быть объектом nomenclature_type")

        self._type = value

    @staticmethod
    def create_product(name: str, full_name: str, group: nomenclature_group_model, unit: unit_model) -> "nomenclature_model":
        """ Фабричный метод: номенклатура типа "Продукт" """
        return nomenclature_model(name, full_name, group, unit, nomenclature_type.PRODUCT)

    @staticmethod
    def create_semi_finished(name: str, full_name: str, group: nomenclature_group_model, unit: unit_model) -> "nomenclature_model":
        """ Фабричный метод: номенклатура типа "Полуфабрикат" """
        return nomenclature_model(name, full_name, group, unit, nomenclature_type.SEMI_FINISHED)

    @staticmethod
    def create_packaging(name: str, full_name: str, group: nomenclature_group_model, unit: unit_model) -> "nomenclature_model":
        """ Фабричный метод: номенклатура типа "Упаковка" """
        return nomenclature_model(name, full_name, group, unit, nomenclature_type.PACKAGING)