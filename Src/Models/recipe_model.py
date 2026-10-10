from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Models.ingredient_model import ingredient_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model


class recipe_model(base_model):
    """
    Доменная модель: Технологическая карта (рецепт)
    Владелец рецепта - номенклатура: готовое блюдо или полуфабрикат
    Вес Брутто и Нетто рецепта - сумма весов всех ингредиентов
    """

    def __init__(self, name: str, owner: nomenclature_model, preparation_method: str = "", portions: int = 1) -> None:
        """
        Инициализирует рецепт

        name: Наименование рецепта
        owner: Номенклатура, которую получаем по рецепту
        preparation_method: Способ приготовления
        portions: Количество порций (целое число больше 0)
        """
        super().__init__()
        self.name = name
        self.owner = owner
        self.preparation_method = preparation_method
        self.portions = portions
        self._ingredients: list[ingredient_model] = []

    @property
    def owner(self) -> nomenclature_model:
        """Возвращает номенклатуру - владельца рецепта"""
        return self._owner

    @owner.setter
    def owner(self, value: nomenclature_model) -> None:
        """Задаёт владельца рецепта"""
        if not isinstance(value, nomenclature_model):
            raise arguments_exception("owner", "Владелец рецепта должен быть объектом nomenclature_model")

        self._owner = value

    @property
    def preparation_method(self) -> str:
        """Возвращает способ приготовления"""
        return self._preparation_method

    @preparation_method.setter
    def preparation_method(self, value: str) -> None:
        """Задаёт способ приготовления (строка, может быть пустой)"""
        if not isinstance(value, str):
            raise arguments_exception("preparation_method", "Способ приготовления должен быть строкой")

        self._preparation_method = value.strip()

    @property
    def portions(self) -> int:
        """Возвращает количество порций"""
        return self._portions

    @portions.setter
    def portions(self, value: int) -> None:
        """
        Задаёт количество порций

        raises arguments_exception: Если передано не целое число или число <= 0
        """
        if isinstance(value, bool) or not isinstance(value, int):
            raise arguments_exception("portions", "Количество порций должно быть целым числом")

        if value <= 0:
            raise arguments_exception("portions", "Количество порций должно быть больше 0")

        self._portions = value

    @property
    def ingredients(self) -> list:
        """Возвращает копию списка ингредиентов (менять состав можно только через add/remove)"""
        return list(self._ingredients)

    def add_ingredient(self, ingredient: ingredient_model) -> None:
        """
        Добавляет ингредиент в рецепт

        raises arguments_exception: Если передан не ingredient_model
        """
        if not isinstance(ingredient, ingredient_model):
            raise arguments_exception("ingredient", "Ингредиент должен быть объектом ingredient_model")

        self._ingredients.append(ingredient)

    def remove_ingredient(self, ingredient: ingredient_model) -> None:
        """ Удаляет ингредиент из рецепта (если его там нет, ничего не происходит) """
        if ingredient in self._ingredients:
            self._ingredients.remove(ingredient)

    @property
    def total_net_weight(self) -> float:
        """Возвращает общий вес Нетто: сумма Нетто всех ингредиентов"""
        return sum(ing.net_weight for ing in self._ingredients)

    @property
    def total_gross_weight(self) -> float:
        """Возвращает общий вес Брутто: сумма Брутто всех ингредиентов"""
        return sum(ing.gross_weight for ing in self._ingredients)

    @staticmethod
    def create_sauce_recipe(sauce: nomenclature_model, chicken: nomenclature_model, mushrooms: nomenclature_model,
                            cream: nomenclature_model, oil: nomenclature_model, garlic: nomenclature_model,
                            salt: nomenclature_model) -> "recipe_model":
        """
        Фабричный метод: рецепт полуфабриката "Сливочно-грибной соус"

        Количество ингредиентов указано в единицах самой номенклатуры
        (сливки в литрах, масло в столовых ложках, соль в чайных ложках)
        и переводится в базовые единицы через ingredient_model.create()
        """
        recipe = recipe_model(
            "Приготовление соуса", sauce,
            "Обжарить чеснок, курицу и шампиньоны, добавить сливки и соль, тушить 3-4 минуты", 1
        )

        recipe.add_ingredient(ingredient_model.create(chicken, 150, 160))
        recipe.add_ingredient(ingredient_model.create(mushrooms, 100, 110))
        recipe.add_ingredient(ingredient_model.create(cream, 0.15, 0.15))   # 0.15 л -> 150 мл
        recipe.add_ingredient(ingredient_model.create(oil, 2, 2))           # 2 ст.л. -> 30 мл
        recipe.add_ingredient(ingredient_model.create(garlic, 5, 7))        # 1 зубчик: 5 г нетто, 7 г брутто
        recipe.add_ingredient(ingredient_model.create(salt, 0.5, 0.5))      # 0.5 ч.л. -> 3.5 г

        return recipe

    @staticmethod
    def create_pasta_recipe(dish: nomenclature_model, pasta: nomenclature_model, sauce_recipe: "recipe_model",
                            parmesan: nomenclature_model, box: nomenclature_model, gram: unit_model) -> "recipe_model":
        """
        Фабричный метод: рецепт готового блюда "Паста сливочная с курицей"

        Содержит полуфабрикат (соус, вес берется из его рецепта) и упаковку

        dish: Номенклатура готового блюда
        sauce_recipe: Рецепт соуса (его владелец - полуфабрикат)
        gram: Единица "грамм" для веса упаковки
        """
        recipe = recipe_model(
            "Сборка пасты", dish,
            "Отварить пасту до состояния альденте, смешать с соусом, посыпать пармезаном, упаковать", 1
        )

        sauce = sauce_recipe.owner

        recipe.add_ingredient(ingredient_model.create(pasta, 100, 100))
        # Полуфабрикат: вес берем из рецепта соуса
        recipe.add_ingredient(ingredient_model(sauce, sauce_recipe.total_net_weight, sauce_recipe.total_gross_weight, sauce.unit))
        recipe.add_ingredient(ingredient_model.create(parmesan, 30, 32))
        # Упаковка: в Нетто блюда не входит (0), в Брутто 20 г для списания
        # Упаковку добавлять необязательно 
        recipe.add_ingredient(ingredient_model(box, 0, 20, gram))

        return recipe