import pytest
from Src.Core.nomenclature_type import nomenclature_type
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager


@pytest.fixture
def storage():
    """ Хранилище после чистого первого старта """
    settings_manager().settings.is_first_start = True

    storage = storage_manager()
    for items in storage.data.values():
        items.clear()

    storage.load()
    return storage


def find_recipe(storage, owner_name: str):
    """ Ищет рецепт по названию номенклатуры-владельца """
    return next((r for r in storage.recipes if r.owner.name == owner_name), None)


def test_first_start_creates_recipes(storage):
    """ После первого старта в хранилище есть рецепты соуса и пасты """
    # Подготовка
    expected_recipes_count = 2
    
    # Действие
    actual_recipes_count = len(storage.recipes)
    sauce = find_recipe(storage, "Сливочно-грибной соус")
    pasta = find_recipe(storage, "Паста сливочная с курицей")

    # Проверка
    assert actual_recipes_count == expected_recipes_count
    assert sauce is not None
    assert pasta is not None


def test_pasta_recipe_has_semi_finished_and_packaging(storage):
    """ Рецепт пасты содержит полуфабрикат и упаковку """
    # Подготовка
    pasta = find_recipe(storage, "Паста сливочная с курицей")
    expected_ingredients_count = 4
    
    # Действие
    types = [ing.nomenclature.type for ing in pasta.ingredients]
    group_name = pasta.owner.group.name

    # Проверка
    assert len(pasta.ingredients) == expected_ingredients_count
    assert nomenclature_type.SEMI_FINISHED in types
    assert nomenclature_type.PACKAGING in types
    assert group_name == "Готовая продукция"


def test_sauce_unit_conversion(storage):
    """ Сливки, масло и соль пересчитаны в базовые единицы через to_base() """
    # Подготовка
    sauce = find_recipe(storage, "Сливочно-грибной соус")
    
    # Действие
    weights = {ing.name: ing.net_weight for ing in sauce.ingredients}

    # Проверка
    assert weights["Сливки 20%"] == pytest.approx(150.0)             # 0.15 л
    assert weights["Масло растительное"] == pytest.approx(30.0)      # 2 ст.л.
    assert weights["Соль"] == pytest.approx(3.5)                     # 0.5 ч.л.


def test_sauce_weights(storage):
    """ Нетто и Брутто соуса """
    # Подготовка
    sauce = find_recipe(storage, "Сливочно-грибной соус")

    # Действие
    net_weight = sauce.total_net_weight
    gross_weight = sauce.total_gross_weight

    # Проверка
    assert net_weight == pytest.approx(438.5)
    assert gross_weight == pytest.approx(460.5)


def test_pasta_weights(storage):
    """ Нетто и Брутто пасты: паста + соус + сыр + упаковка """
    # Подготовка
    pasta = find_recipe(storage, "Паста сливочная с курицей")

    # Действие
    net_weight = pasta.total_net_weight
    gross_weight = pasta.total_gross_weight

    # Проверка
    # Нетто: 100 + 438.5 + 30 + 0
    assert net_weight == pytest.approx(568.5)
    # Брутто: 100 + 460.5 + 32 + 20
    assert gross_weight == pytest.approx(612.5)


def test_pasta_weights_change_when_ingredient_removed(storage):
    """ Исключение упаковки уменьшает Брутто на 20, Нетто не меняется """
    # Подготовка
    pasta = find_recipe(storage, "Паста сливочная с курицей")
    box = next(ing for ing in pasta.ingredients if ing.nomenclature.type == nomenclature_type.PACKAGING)

    # Действие
    pasta.remove_ingredient(box)
    new_net_weight = pasta.total_net_weight
    new_gross_weight = pasta.total_gross_weight

    # Проверка
    assert new_net_weight == pytest.approx(568.5)
    assert new_gross_weight == pytest.approx(592.5)


def test_first_start_runs_once(storage):
    """ Повторная загрузка не дублирует рецепты (флаг первого старта выключен) """
    # Подготовка
    expected_recipes_count = 2

    # Действие
    storage.load()  # Пытаемся загрузить данные еще раз
    actual_recipes_count = len(storage.recipes)

    # Проверка
    assert actual_recipes_count == expected_recipes_count


def test_units_in_storage_share_base_units(storage):
    """ Литр ссылается на тот же миллилитр, который лежит в хранилище """
    # Подготовка
    liter = next(u for u in storage.units if u.name == "Литр (л)")

    # Действие
    # Ищем, есть ли в списке единиц тот самый объект, на который ссылается литр
    is_shared = any(u is liter.base_unit for u in storage.units)

    # Проверка
    assert is_shared is True