import pytest
from Src.Core.nomenclature_type import nomenclature_type
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager


@pytest.fixture
def storage():
    """ Подготовка: пустое хранилище и включенный флаг первого старта """
    settings_manager().settings.is_first_start = True

    storage = storage_manager()
    for items in storage.data.values():
        items.clear()

    return storage


def find_recipe(storage, owner_name: str):
    """ Ищет рецепт в хранилище по названию номенклатуры-владельца """
    return next((r for r in storage.recipes if r.owner.name == owner_name), None)


def test_first_start_creates_recipes(storage):
    """ После первого старта в хранилище есть рецепты соуса и пасты """
    # Подготовка: хранилище пустое

    # Действие: первый старт
    storage.load()

    # Проверка
    assert len(storage.recipes) == 2
    assert find_recipe(storage, "Сливочно-грибной соус") is not None
    assert find_recipe(storage, "Паста сливочная с курицей") is not None


def test_pasta_recipe_has_semi_finished_and_packaging(storage):
    """ Рецепт пасты содержит полуфабрикат и упаковку """
    # Подготовка: хранилище пустое

    # Действие: первый старт и поиск рецепта пасты
    storage.load()
    pasta = find_recipe(storage, "Паста сливочная с курицей")
    types = [ing.nomenclature.type for ing in pasta.ingredients]

    # Проверка
    assert len(pasta.ingredients) == 4
    assert nomenclature_type.SEMI_FINISHED in types
    assert nomenclature_type.PACKAGING in types
    assert pasta.owner.group.name == "Готовая продукция"


def test_pasta_uses_sauce_as_composite_recipe(storage):
    """ Полуфабрикат в пасте - это ссылка на рецепт соуса, а не просто число """
    # Подготовка: хранилище пустое

    # Действие: первый старт, поиск соуса и составного ингредиента в пасте
    storage.load()
    sauce = find_recipe(storage, "Сливочно-грибной соус")
    pasta = find_recipe(storage, "Паста сливочная с курицей")
    sauce_ingredient = next(ing for ing in pasta.ingredients if ing.nomenclature.type == nomenclature_type.SEMI_FINISHED)

    # Проверка: ссылка на рецепт, 1 порция из 2, Брутто по пропорции
    assert sauce_ingredient.recipe is sauce
    assert sauce.portions == 2
    assert sauce_ingredient.net_weight == pytest.approx(219.25)      # 438.5 / 2
    assert sauce_ingredient.gross_weight == pytest.approx(230.25)    # 460.5 * 219.25 / 438.5


def test_sauce_unit_conversion(storage):
    """ Сливки, масло и соль пересчитаны в базовые единицы через to_base() """
    # Подготовка: хранилище пустое

    # Действие: первый старт и сбор Нетто ингредиентов соуса по названиям
    storage.load()
    sauce = find_recipe(storage, "Сливочно-грибной соус")
    weights = {ing.name: ing.net_weight for ing in sauce.ingredients}

    # Проверка
    assert weights["Сливки 20%"] == pytest.approx(150.0)             # 0.15 л * 1000
    assert weights["Масло растительное"] == pytest.approx(30.0)      # 2 ст.л. * 15
    assert weights["Соль"] == pytest.approx(3.5)                     # 0.5 ч.л. * 7


def test_sauce_weights(storage):
    """ Нетто и Брутто рецепта соуса """
    # Подготовка: хранилище пустое (фикстура storage)

    # Действие: первый старт
    storage.load()
    sauce = find_recipe(storage, "Сливочно-грибной соус")

    # Проверка
    assert sauce.total_net_weight == pytest.approx(438.5)     # 150 + 100 + 150 + 30 + 5 + 3.5
    assert sauce.total_gross_weight == pytest.approx(460.5)   # 160 + 110 + 150 + 30 + 7 + 3.5


def test_pasta_weights(storage):
    """ Нетто и Брутто пасты: паста + 1 порция соуса + сыр + упаковка """
    # Подготовка: хранилище пустое

    # Действие: первый старт
    storage.load()
    pasta = find_recipe(storage, "Паста сливочная с курицей")

    # Проверка
    assert pasta.total_net_weight == pytest.approx(349.25)    # 100 + 219.25 + 30 + 0
    assert pasta.total_gross_weight == pytest.approx(382.25)  # 100 + 230.25 + 32 + 20


def test_pasta_weights_after_removing_packaging(storage):
    """ Исключение упаковки уменьшает Брутто на 20 г, Нетто не меняется """
    # Подготовка: выполнен первый старт, найдены паста и упаковка в ее составе
    storage.load()
    pasta = find_recipe(storage, "Паста сливочная с курицей")
    packaging = next(ing for ing in pasta.ingredients if ing.nomenclature.type == nomenclature_type.PACKAGING)

    # Действие: исключаем упаковку из рецепта
    pasta.remove_ingredient(packaging)

    # Проверка
    assert len(pasta.ingredients) == 3
    assert pasta.total_net_weight == pytest.approx(349.25)
    assert pasta.total_gross_weight == pytest.approx(362.25)  # 382.25 - 20


def test_first_start_runs_once(storage):
    """ Повторная загрузка не дублирует рецепты: флаг первого старта выключается после первого запуска """
    # Подготовка: первый старт уже выполнен
    storage.load()

    # Действие: загружаем хранилище второй раз
    storage.load()

    # Проверка: рецептов по-прежнему два
    assert len(storage.recipes) == 2


def test_units_in_storage_share_base_units(storage):
    """ Литр в хранилище ссылается на тот же миллилитр, который лежит в списке единиц """
    # Подготовка: хранилище пустое

    # Действие: первый старт и поиск литра
    storage.load()
    liter = next(u for u in storage.units if u.name == "Литр (л)")

    # Проверка: базовая единица литра - один из объектов в хранилище
    assert any(u is liter.base_unit for u in storage.units)