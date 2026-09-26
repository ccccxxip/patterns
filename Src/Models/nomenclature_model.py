from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.constants import FULL_NAME_MAX_LENGTH
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model


class nomenclature_model(base_model):
    """
    Модель данных "Номенклатура"
    Наследуется от base_model
    Включает в себя полное наименование, ссылку на группу номенклатуры и единицу измерения
    """

    def __init__(self, name: str, full_name: str, group: nomenclature_group_model, unit: unit_model) -> None:
        """
        Инициализирует экземпляр модели номенклатуры

        name: Обычное наименование (до 50 символов, валидируется в base_model)
        full_name: Полное наименование (до 255 символов)
        group: Группа номенклатуры (экземпляр nomenclature_group_model)
        unit: Единица измерения (экземпляр unit_model)
        """
        super().__init__()
        self.name = name
        self.full_name = full_name
        self.group = group
        self.unit = unit

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