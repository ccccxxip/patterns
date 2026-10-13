import pytest
from Src.Core.exception import arguments_exception
from Src.Core.nomenclature_type import nomenclature_type
from Src.Models.recipe_model import recipe_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model


def make_product(name: str, unit: unit_model) -> nomenclature_model:
    """ Создает продукт в группе "Сырье" """
    return nomenclature_model.create_product(name, name, nomenclature_group_model.create_raw(), unit)


def make_sauce_recipe() -> recipe_model:
    """ Создает рецепт соуса на 2 порции: Нетто 438.5 г, Брутто 460.5 г """
    g = unit_model.create_gram()
    ml = unit_model.create_milliliter()
    raw = nomenclature_group_model.create_raw()

    chicken = nomenclature_model.create_product("Куриное филе", "Куриное филе охл.", raw, g)
    mushrooms = nomenclature_model.create_product("Шампиньоны свежие", "Шампиньоны свежие", raw, g)
    cream = nomenclature_model.create_product("Сливки 20%", "Сливки 20%", raw, unit_model.create_liter(ml))
    oil = nomenclature_model.create_product("Масло растительное", "Масло растительное", raw, unit_model.create_tablespoon(ml))
    garlic = nomenclature_model.create_product("Чеснок", "Чеснок", raw, g)
    salt = nomenclature_model.create_product("Соль", "Соль пищевая", raw, unit_model.create_teaspoon(g))
    sauce = nomenclature_model.create_semi_finished(
        "Сливочно-грибной соус", "Сливочно-грибной соус (п/ф)", nomenclature_group_model.create_semi_finished(), g
    )

    return recipe_model.create_sauce_recipe(sauce, chicken, mushrooms, cream, oil, garlic, salt)


def make_pasta_recipe(sauce_recipe: recipe_model) -> recipe_model:
    """ Создает рецепт пасты на основе рецепта соуса: Нетто 349.25 г, Брутто 382.25 г """
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()

    pasta = nomenclature_model.create_product("Паста (феттуччине)", "Паста (феттуччине)", raw, g)
    parmesan = nomenclature_model.create_product("Сыр Пармезан", "Сыр Пармезан", raw, g)
    box = nomenclature_model.create_packaging(
        "Контейнер крафтовый", "Контейнер крафтовый", nomenclature_group_model.create_packaging(), unit_model.create_piece()
    )
    dish = nomenclature_model.create_product(
        "Паста сливочная с курицей", "Паста сливочная с курицей", nomenclature_group_model.create_finished(), unit_model.create_piece()
    )

    return recipe_model.create_pasta_recipe(dish, pasta, sauce_recipe, parmesan, box, g)


def test_total_weights_after_adding_ingredients():
    """ Нетто и Брутто рецепта равны сумме весов добавленных ингредиентов """
    # Подготовка: сахар 100/110 г и вода 200/200 г
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)
    water = make_product("Вода", g)
    recipe = recipe_model("Сироп", sugar)

    # Действие: добавляем два ингредиента
    recipe.add_ingredient(ingredient_model(sugar, 100.0, 110.0, g))
    recipe.add_ingredient(ingredient_model(water, 200.0, 200.0, g))

    # Проверка : Нетто 100 + 200, Брутто 110 + 200
    assert recipe.total_net_weight == pytest.approx(300.0)
    assert recipe.total_gross_weight == pytest.approx(310.0)


def test_total_weights_after_removing_ingredient():
    """ После исключения ингредиента Нетто и Брутто пересчитываются """
    # Подготовка: рецепт с двумя ингредиентами
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)
    water = make_product("Вода", g)
    recipe = recipe_model("Сироп", sugar)
    sugar_ingredient = ingredient_model(sugar, 100.0, 110.0, g)
    recipe.add_ingredient(sugar_ingredient)
    recipe.add_ingredient(ingredient_model(water, 200.0, 200.0, g))

    # Действие: исключаем сахар из рецепта
    recipe.remove_ingredient(sugar_ingredient)

    # Проверка: остается только вода
    assert len(recipe.ingredients) == 1
    assert recipe.total_net_weight == pytest.approx(200.0)
    assert recipe.total_gross_weight == pytest.approx(200.0)


def test_total_weights_after_adding_ingredient_to_existing_recipe():
    """ Добавление нового ингредиента в уже готовый рецепт увеличивает Нетто и Брутто """
    # Подготовка: рецепт с одним ингредиентом (сахар 100/110 г)
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)
    recipe = recipe_model("Сироп", sugar)
    recipe.add_ingredient(ingredient_model(sugar, 100, 110, g))

    # Действие: добавляем еще один ингредиент (лимонная кислота 5/5 г)
    recipe.add_ingredient(ingredient_model(make_product("Лимонная кислота", g), 5, 5, g))

    # Проверка: Нетто 100 + 5, Брутто 110 + 5
    assert recipe.total_net_weight == pytest.approx(105.0)
    assert recipe.total_gross_weight == pytest.approx(115.0)


def test_empty_recipe_weights_are_zero():
    """ В рецепте без ингредиентов Нетто и Брутто равны 0 """
    # Подготовка: рецепт без ингредиентов
    g = unit_model.create_gram()
    recipe = recipe_model("Пусто", make_product("Сахар", g))

    # Действие: запрашиваем веса
    net = recipe.total_net_weight
    gross = recipe.total_gross_weight

    # Проверка
    assert net == 0
    assert gross == 0


def test_remove_missing_ingredient_does_nothing():
    """ Удаление ингредиента, которого нет в рецепте, ничего не меняет и не вызывает ошибку """
    # Подготовка: рецепт с одним ингредиентом и другой ингредиент, которого в рецепте нет
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)
    recipe = recipe_model("Сироп", sugar)
    recipe.add_ingredient(ingredient_model(sugar, 100, 110, g))
    foreign_ingredient = ingredient_model(sugar, 1, 1, g)

    # Действие: пытаемся удалить чужой ингредиент
    recipe.remove_ingredient(foreign_ingredient)

    # Проверка: состав и вес не изменились
    assert len(recipe.ingredients) == 1
    assert recipe.total_net_weight == pytest.approx(100.0)


def test_add_invalid_ingredient_raises():
    """ В рецепт нельзя добавить объект, который не является ингредиентом """
    # Подготовка
    g = unit_model.create_gram()
    recipe = recipe_model("Сироп", make_product("Сахар", g))

    # Действие и проверка: добавляем строку вместо ингредиента
    with pytest.raises(arguments_exception):
        recipe.add_ingredient("не ингредиент")


def test_recipe_owner_must_be_nomenclature():
    """ Владельцем рецепта может быть только номенклатура """
    # Действие и проверка: передаем строку вместо номенклатуры
    with pytest.raises(arguments_exception):
        recipe_model("Сироп", "не номенклатура")


def test_recipe_portions_must_be_positive():
    """ Количество порций должно быть больше 0 """
    # Подготовка
    sugar = make_product("Сахар", unit_model.create_gram())

    # Действие и проверка: 0 порций
    with pytest.raises(arguments_exception):
        recipe_model("Сироп", sugar, "", 0)


def test_recipe_portions_must_be_integer():
    """ Количество порций должно быть целым числом """
    # Подготовка
    sugar = make_product("Сахар", unit_model.create_gram())

    # Действие и проверка: 1.5 порции
    with pytest.raises(arguments_exception):
        recipe_model("Сироп", sugar, "", 1.5)


def test_ingredient_weight_cannot_be_negative():
    """ Вес ингредиента не может быть отрицательным """
    # Подготовка
    g = unit_model.create_gram()
    sugar = make_product("Сахар", g)

    # Действие и проверка: отрицательное Нетто
    with pytest.raises(arguments_exception):
        ingredient_model(sugar, -1, 1, g)


def test_ingredient_nomenclature_must_be_nomenclature():
    """ Ингредиент создается только на основе номенклатуры """
    # Подготовка 
    g = unit_model.create_gram()

    # Действие и проверка: строка вместо номенклатуры
    with pytest.raises(arguments_exception):
        ingredient_model("не номенклатура", 1, 1, g)



def test_ingredient_create_converts_to_base_unit():
    """ Фабрика ingredient_model.create переводит количество в базовую единицу (0.15 л -> 150 мл) """
    # Подготовка: сливки, единица номенклатуры - литр, базовая - миллилитр
    ml = unit_model.create_milliliter()
    cream = make_product("Сливки", unit_model.create_liter(ml))

    # Действие: создаем ингредиент на 0.15 л
    ingredient = ingredient_model.create(cream, 0.15, 0.15)

    # Проверка: веса в миллилитрах, единица - базовая
    assert ingredient.net_weight == pytest.approx(150.0)
    assert ingredient.gross_weight == pytest.approx(150.0)
    assert ingredient.unit is ml


def test_unit_factories_use_given_base_unit():
    """ Производные единицы ссылаются на переданную базовую единицу, а не на ее копию """
    # Подготовка: базовые единицы
    g = unit_model.create_gram()
    ml = unit_model.create_milliliter()

    # Действие: создаем производные единицы от них
    kilogram = unit_model.create_kilogram(g)
    liter = unit_model.create_liter(ml)
    tablespoon = unit_model.create_tablespoon(ml)
    teaspoon = unit_model.create_teaspoon(g)

    # Проверка: ссылка именно на переданный объект
    assert kilogram.base_unit is g
    assert liter.base_unit is ml
    assert tablespoon.base_unit is ml
    assert teaspoon.base_unit is g


def test_nomenclature_factories_set_type():
    """ Фабрики номенклатуры задают тип: продукт, полуфабрикат, упаковка """
    # Подготовка
    g = unit_model.create_gram()
    group = nomenclature_group_model.create_raw()

    # Действие: создаем номенклатуру тремя фабриками
    product = nomenclature_model.create_product("А", "А", group, g)
    semi_finished = nomenclature_model.create_semi_finished("Б", "Б", group, g)
    packaging = nomenclature_model.create_packaging("В", "В", group, g)

    # Проверка
    assert product.type == nomenclature_type.PRODUCT
    assert semi_finished.type == nomenclature_type.SEMI_FINISHED
    assert packaging.type == nomenclature_type.PACKAGING


def test_composite_recipe_scales_by_quantity():
    """ Из рецепта соуса взяли четверть: расход пересчитывается пропорционально (коэффициент 0.25) """
    # Подготовка: рецепт соуса (Нетто 438.5, Брутто 460.5) и четверть его Нетто
    sauce = make_sauce_recipe()
    quarter = sauce.total_net_weight / 4

    # Действие: создаем составной ингредиент на четверть соуса
    ingredient = ingredient_model.create_from_recipe(sauce, quarter)

    # Проверка
    assert ingredient.recipe is sauce
    assert ingredient.net_weight == pytest.approx(109.625)       # 438.5 / 4
    assert ingredient.gross_weight == pytest.approx(115.125)     # 460.5 * 109.625 / 438.5


def test_pasta_weights_use_sauce_proportion():
    """ В пасту идет 1 порция соуса из 2: Брутто соуса считается по пропорции, а не целиком """
    # Подготовка: рецепт соуса на 2 порции
    sauce = make_sauce_recipe()

    # Действие: собираем рецепт пасты
    pasta = make_pasta_recipe(sauce)

    # Проверка
    assert pasta.total_net_weight == pytest.approx(349.25)       # 100 + 219.25 + 30 + 0
    assert pasta.total_gross_weight == pytest.approx(382.25)     # 100 + 230.25 + 32 + 20


def test_nested_composite_recipe():
    """ Рецепт внутри рецепта внутри рецепта: пересчет работает по цепочке (набор -> паста -> соус) """
    # Подготовка: рецепт пасты (Нетто 349.25, Брутто 382.25) и пустой рецепт набора на двоих
    g = unit_model.create_gram()
    pasta = make_pasta_recipe(make_sauce_recipe())
    dish = nomenclature_model.create_product(
        "Набор на двоих", "Набор из двух паст", nomenclature_group_model.create_finished(), g
    )
    set_for_two = recipe_model("Набор на двоих", dish)

    # Действие: набор берет две порции пасты
    set_for_two.add_ingredient(ingredient_model.create_from_recipe(pasta, pasta.total_net_weight * 2))

    # Проверка: все веса вдвое больше, чем у одной пасты
    assert set_for_two.total_net_weight == pytest.approx(698.5)       # 349.25 * 2
    assert set_for_two.total_gross_weight == pytest.approx(764.5)     # 382.25 * 2


def test_composite_gross_recalculates_when_sub_recipe_changes():
    """ Если в соус добавить ингредиент, Брутто соуса внутри пасты пересчитывается """
    # Подготовка: паста на основе соуса
    g = unit_model.create_gram()
    sauce = make_sauce_recipe()
    pasta = make_pasta_recipe(sauce)

    # Действие: добавляем в соус перец (Нетто 2 г, Брутто 2 г)
    sauce.add_ingredient(ingredient_model(make_product("Перец", g), 2, 2, g))

    # Проверка: соус теперь Нетто 440.5, Брутто 462.5, в пасту идет те же 219.25 г
    sauce_in_pasta = next(ing for ing in pasta.ingredients if ing.recipe is sauce)
    expected_sauce_gross = 462.5 * 219.25 / 440.5
    assert sauce_in_pasta.net_weight == pytest.approx(219.25)
    assert sauce_in_pasta.gross_weight == pytest.approx(expected_sauce_gross)
    assert pasta.total_gross_weight == pytest.approx(100 + expected_sauce_gross + 32 + 20)


def test_recipe_cannot_contain_itself_directly():
    """ Рецепт нельзя включить в самого себя """
    # Подготовка
    sauce = make_sauce_recipe()

    # Действие и проверка: добавляем соус в соус
    with pytest.raises(arguments_exception):
        sauce.add_ingredient(ingredient_model.create_from_recipe(sauce, 10))


def test_recipe_cannot_contain_itself_through_nested_recipe():
    """ Рецепт нельзя включить в себя через вложенный рецепт (соус -> паста -> соус) """
    # Подготовка: паста уже содержит соус
    sauce = make_sauce_recipe()
    pasta = make_pasta_recipe(sauce)

    # Действие и проверка: пытаемся добавить пасту в соус, получился бы цикл
    with pytest.raises(arguments_exception):
        sauce.add_ingredient(ingredient_model.create_from_recipe(pasta, 10))


def test_composite_from_empty_recipe_raises():
    """ Нельзя взять часть рецепта, у которого Нетто равно 0: пропорцию не посчитать """
    # Подготовка: рецепт без ингредиентов
    g = unit_model.create_gram()
    empty = recipe_model("Пусто", make_product("Заготовка", g))

    # Действие и проверка
    with pytest.raises(arguments_exception):
        ingredient_model.create_from_recipe(empty, 10)


def test_composite_owner_must_match_recipe():
    """ Номенклатура составного ингредиента должна совпадать с владельцем его рецепта """
    # Подготовка: рецепт соуса и посторонняя номенклатура
    g = unit_model.create_gram()
    sauce = make_sauce_recipe()
    foreign = make_product("Другая номенклатура", g)

    # Действие и проверка
    with pytest.raises(arguments_exception):
        ingredient_model(foreign, 80, 0, g, sauce)


def test_composite_from_not_recipe_raises():
    """ Составной ингредиент создается только из рецепта """
    # Действие и проверка: строка вместо рецепта
    with pytest.raises(arguments_exception):
        ingredient_model.create_from_recipe("не рецепт", 10)