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

    # Фабричные методы
    # Производные единицы принимают базовую единицу параметром, чтобы в хранилище
    # у литра, ложек и килограмма была ссылка на тот же объект (мл или г), а не на копию.
    # Если базовую единицу не передать, она создаётся внутри

    @staticmethod
    def create_gram() -> "unit_model":
        """ Фабричный метод: грамм (базовая единица массы) """
        return unit_model("Грамм (г)", 1.0)

    @staticmethod
    def create_milliliter() -> "unit_model":
        """ Фабричный метод: миллилитр (базовая единица объема) """
        return unit_model("Миллилитр (мл)", 1.0)

    @staticmethod
    def create_piece() -> "unit_model":
        """ Фабричный метод: штука """
        return unit_model("Штука (шт)", 1.0)

    @staticmethod
    def create_kilogram(gram: "unit_model" = None) -> "unit_model":
        """ Фабричный метод: килограмм (1000 г) """
        return unit_model("Килограмм (кг)", 1000.0, gram if gram is not None else unit_model.create_gram())

    @staticmethod
    def create_liter(milliliter: "unit_model" = None) -> "unit_model":
        """ Фабричный метод: литр (1000 мл) """
        return unit_model("Литр (л)", 1000.0, milliliter if milliliter is not None else unit_model.create_milliliter())

    @staticmethod
    def create_tablespoon(milliliter: "unit_model" = None) -> "unit_model":
        """ Фабричный метод: столовая ложка (15 мл) """
        return unit_model("Столовая ложка (ст.л.)", 15.0, milliliter if milliliter is not None else unit_model.create_milliliter())

    @staticmethod
    def create_teaspoon(gram: "unit_model" = None) -> "unit_model":
        """ Фабричный метод: чайная ложка соли (7 г) """
        return unit_model("Чайная ложка (ч.л.)", 7.0, gram if gram is not None else unit_model.create_gram())