from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model


class ingredient_model(base_model):
    """
    Доменная модель: Строка технологической карты (Ингредиент)
    Хранит веса Брутто и Нетто для конкретной номенклатуры

    Ингредиент бывает двух видов:
    - простой (продукт, упаковка): веса заданы напрямую
    - составной (полуфабрикат или другое блюдо): ссылается на свой рецепт (recipe),
      Нетто - сколько взято, Брутто пересчитывается пропорционально по рецепту
    """

    def __init__(self, nomenclature: nomenclature_model, net_weight: float, gross_weight: float, unit: unit_model,
                 recipe=None) -> None:
        """
        Инициализирует ингредиент

        nomenclature: Номенклатура (продукт, полуфабрикат или упаковка)
        net_weight: Вес Нетто (без отходов)
        gross_weight: Вес Брутто (с отходами), для составного ингредиента не используется
        unit: Единица измерения, в которой указаны веса
        recipe: Рецепт полуфабриката (recipe_model) для составного ингредиента, иначе None
        """
        super().__init__()
        self.nomenclature = nomenclature
        self.name = nomenclature.name
        self.recipe = recipe
        self.net_weight = net_weight
        self.gross_weight = gross_weight
        self.unit = unit

    @property
    def recipe(self):
        """Возвращает рецепт составного ингредиента (для простого - None)"""
        return self._recipe

    @recipe.setter
    def recipe(self, value) -> None:
        """
        Задаёт рецепт составного ингредиента

        raises arguments_exception: Если передан не recipe_model или владелец рецепта не совпадает с номенклатурой
        """
        if value is None:
            self._recipe = None
            return

        from Src.Models.recipe_model import recipe_model

        if not isinstance(value, recipe_model):
            raise arguments_exception("recipe", "Рецепт должен быть объектом recipe_model")

        if value.owner != self.nomenclature:
            raise arguments_exception("recipe", "Владелец рецепта должен совпадать с номенклатурой ингредиента")

        self._recipe = value

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
        """
        Возвращает вес Брутто

        Для составного ингредиента считается по пропорции:
        Брутто рецепта * (взятое Нетто / Нетто рецепта)
        """
        if self._recipe is None:
            return self._gross_weight

        recipe_net = self._recipe.total_net_weight
        if recipe_net == 0:
            return 0.0

        return self._recipe.total_gross_weight * self.net_weight / recipe_net

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

        Количество переводится в базовую единицу через unit.to_base(),
        например 0.15 л сливок становится 150 мл

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

    @staticmethod
    def create_from_recipe(recipe, net_quantity: float) -> "ingredient_model":
        """
        Фабричный метод: составной ингредиент (полуфабрикат или другое блюдо по его рецепту)

        recipe: Рецепт полуфабриката (его владелец становится номенклатурой ингредиента)
        net_quantity: Сколько Нетто этого полуфабриката берется в блюдо
        raises arguments_exception: Если передан не рецепт или Нетто рецепта равно 0 (нечего пересчитывать)
        """
        from Src.Models.recipe_model import recipe_model

        if not isinstance(recipe, recipe_model):
            raise arguments_exception("recipe", "Рецепт должен быть объектом recipe_model")

        if recipe.total_net_weight <= 0:
            raise arguments_exception("recipe", "Нетто рецепта должно быть больше 0, иначе нельзя сделать пересчет")

        return ingredient_model(recipe.owner, net_quantity, 0, recipe.owner.unit, recipe)