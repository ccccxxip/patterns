from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception


class unit_model(base_model):
    """
    Модель данных "Единица измерения"
    Наследуется от base_model
    Хранит базовую единицу измерения и коэффициент пересчета в неё
    """

    def __init__(self, name: str, ratio: float, base_unit: "unit_model" = None) -> None:
        """
        Инициализирует экземпляр единицы измерения

        name: Наименование единицы измерения
        ratio: Коэффициент пересчета в базовую единицу измерения
        base_unit: Ссылка на базовую единицу измерения (экземпляр unit_model)
        """
        super().__init__()
        self.name = name
        self.ratio = ratio
        self.base_unit = base_unit if base_unit is not None else self

    @property
    def ratio(self) -> float:
        """Возвращает коэффициент пересчета в базовую единицу измерения"""
        return self._ratio

    @ratio.setter
    def ratio(self, value: float) -> None:
        """
        Задаёт коэффициент пересчета

        value: Положительное число (int или float)
        raises arguments_exception: Если передано не число или число <= 0
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise arguments_exception("ratio", "Коэффициент пересчета должен быть числом")

        if value <= 0:
            raise arguments_exception("ratio", "Коэффициент пересчета должен быть положительным числом")

        self._ratio = float(value)

    @property
    def base_unit(self) -> "unit_model":
        """Возвращает базовую единицу измерения"""
        return self._base_unit

    @base_unit.setter
    def base_unit(self, value: "unit_model") -> None:
        """
        Задаёт базовую единицу измерения

        value: Экземпляр класса unit_model
        raises arguments_exception: Если передан объект другого типа
        """
        if not isinstance(value, unit_model):
            raise arguments_exception("base_unit", "Базовая единица измерения должна быть объектом unit_model")

        self._base_unit = value

    def to_base(self, quantity: float) -> float:
        """
        Переводит количество в текущей единице измерения в количество в базовой единице измерения

        quantity: Количество для пересчета
        return: Значение, переведенное в базовую единицу измерения
        raises arguments_exception: Если количество не является числом
        """
        if isinstance(quantity, bool) or not isinstance(quantity, (int, float)):
            raise arguments_exception("quantity", "Количество должно быть числом")

        return quantity * self.ratio