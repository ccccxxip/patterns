import pytest
from Src.Core.exception import arguments_exception
from Src.Core.nomenclature_type import nomenclature_type
from Src.Models.recipe_model import recipe_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model


def make_product(name: str, unit: unit_model) -> nomenclature_model:
    """ Вспомогательная функция: продукт в группе 'Сырье' """
    return nomenclature_model.create_product(name, name, nomenclature_group_model.create_raw(), unit)


def test_recipe_net_and_gross_calculation():
    """ Нетто и Брутто считаются как сумма ингредиентов, в том числе после добавления и удаления """
    # Подготовка
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)
    water = make_product("Вода", g)

    ing1 = ingredient_model(sugar, 100.0, 110.0, g)
    ing2 = ingredient_model(water, 200.0, 200.0, g)
    recipe = recipe_model("Сироп", sugar)

    # Действие: добавляем
    recipe.add_ingredient(ing1)
    recipe.add_ingredient(ing2)
    net_weight_added = recipe.total_net_weight
    gross_weight_added = recipe.total_gross_weight

    # Проверка 1
    assert net_weight_added == pytest.approx(300.0)
    assert gross_weight_added == pytest.approx(310.0)

    # Действие: удаляем
    recipe.remove_ingredient(ing1)
    net_weight_removed = recipe.total_net_weight
    gross_weight_removed = recipe.total_gross_weight

    # Проверка 2
    assert net_weight_removed == pytest.approx(200.0)
    assert gross_weight_removed == pytest.approx(200.0)


def test_add_ingredient_after_creation_changes_weight():
    """ Добавление нового ингредиента в готовый рецепт пересчитывает вес """
    # Подготовка
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)
    recipe = recipe_model("Сироп", sugar)
    recipe.add_ingredient(ingredient_model(sugar, 100, 110, g))
    new_ingredient = ingredient_model(make_product("Лимонная кислота", g), 5, 5, g)

    # Действие
    recipe.add_ingredient(new_ingredient)
    net_weight = recipe.total_net_weight
    gross_weight = recipe.total_gross_weight

    # Проверка
    assert net_weight == pytest.approx(105.0)
    assert gross_weight == pytest.approx(115.0)


def test_empty_recipe_weights_are_zero():
    """ В пустом рецепте Нетто и Брутто равны 0 """
    # Подготовка
    g = unit_model.create_gram()
    recipe = recipe_model("Пусто", make_product("Сахар", g))

    # Действие
    net_weight = recipe.total_net_weight
    gross_weight = recipe.total_gross_weight

    # Проверка
    assert net_weight == 0
    assert gross_weight == 0


def test_remove_missing_ingredient_does_nothing():
    """ Удаление ингредиента, которого нет в рецепте, ничего не ломает """
    # Подготовка
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)
    recipe = recipe_model("Сироп", sugar)
    recipe.add_ingredient(ingredient_model(sugar, 100, 110, g))
    missing_ingredient = ingredient_model(sugar, 1, 1, g)

    # Действие
    recipe.remove_ingredient(missing_ingredient)
    ingredients_count = len(recipe.ingredients)
    net_weight = recipe.total_net_weight

    # Проверка
    assert ingredients_count == 1
    assert net_weight == pytest.approx(100.0)


def test_add_invalid_ingredient_raises():
    """ В рецепт нельзя добавить объект другого типа """
    # Подготовка
    g = unit_model.create_gram()
    recipe = recipe_model("Сироп", make_product("Сахар", g))
    invalid_ingredient = "не ингредиент"

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        recipe.add_ingredient(invalid_ingredient)


def test_recipe_validation():
    """ Проверка владельца и количества порций """
    # Подготовка
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        recipe_model("Сироп", "не номенклатура")
        
    with pytest.raises(arguments_exception):
        recipe_model("Сироп", sugar, "", 0)
        
    with pytest.raises(arguments_exception):
        recipe_model("Сироп", sugar, "", 1.5)


def test_ingredient_validation():
    """ Вес не может быть отрицательным, номенклатура должна быть номенклатурой """
    # Подготовка
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        ingredient_model(sugar, -1, 1, g)
        
    with pytest.raises(arguments_exception):
        ingredient_model("не номенклатура", 1, 1, g)


def test_ingredient_create_converts_to_base_unit():
    """ Фабрика ingredient_model.create переводит количество в базовую единицу """
    # Подготовка
    ml = unit_model.create_milliliter()
    cream = make_product("Сливки", unit_model.create_liter(ml))

    # Действие
    ingredient = ingredient_model.create(cream, 0.15, 0.15)
    net_weight = ingredient.net_weight
    gross_weight = ingredient.gross_weight
    base_unit = ingredient.unit

    # Проверка
    assert net_weight == pytest.approx(150.0)
    assert gross_weight == pytest.approx(150.0)
    assert base_unit is ml


def test_unit_factories_use_given_base_unit():
    """ Производные единицы ссылаются на переданную базовую, а не на копию """
    # Подготовка
    g = unit_model.create_gram()
    ml = unit_model.create_milliliter()

    # Действие
    kg_base = unit_model.create_kilogram(g).base_unit
    l_base = unit_model.create_liter(ml).base_unit
    tbsp_base = unit_model.create_tablespoon(ml).base_unit
    tsp_base = unit_model.create_teaspoon(g).base_unit

    # Проверка
    assert kg_base is g
    assert l_base is ml
    assert tbsp_base is ml
    assert tsp_base is g


def test_nomenclature_factories_set_type():
    """ Фабрики номенклатуры задают тип: продукт, полуфабрикат, упаковка """
    # Подготовка
    g = unit_model.create_gram()
    group = nomenclature_group_model.create_raw()

    # Действие
    product_type = nomenclature_model.create_product("А", "А", group, g).type
    semi_finished_type = nomenclature_model.create_semi_finished("Б", "Б", group, g).type
    packaging_type = nomenclature_model.create_packaging("В", "В", group, g).type

    # Проверка
    assert product_type == nomenclature_type.PRODUCT
    assert semi_finished_type == nomenclature_type.SEMI_FINISHED
    assert packaging_type == nomenclature_type.PACKAGING