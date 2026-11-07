import os
import pytest
from Src.Core.exception import arguments_exception
from Src.Core.nomenclature_type import nomenclature_type
from Src.Logics.convert_factory import convert_factory
from Src.Logics.mapping_factory import mapping_factory
from Src.Logics.storage_manager import storage_manager
from Src.Logics.settings_manager import settings_manager
from Src.Dtos.storage_dto import (
    warehouse_dto,
    unit_dto,
    nomenclature_group_dto,
    nomenclature_dto,
    ingredient_dto,
    recipe_dto,
    storage_dto
)
from Src.Models.warehouse_model import warehouse_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model
from Src.Models.ingredient_model import ingredient_model


def test_mapping_factory_map_warehouse():
    """
    Сценарий: Десериализация warehouse_dto в доменную модель warehouse_model через метод map
    Ожидаемый результат: Создается объект склада с сохраненными id, наименованием и адресом
    """
    # Подготовка
    dto = warehouse_dto(id="test-wh-id", name="Склад №1", address="ул. Ленина, 1")
    factory = mapping_factory()

    # Действие
    model = factory.map(dto)

    # Проверка
    assert isinstance(model, warehouse_model)
    assert model.id == "test-wh-id"
    assert model.name == "Склад №1"
    assert model.address == "ул. Ленина, 1"


def test_mapping_factory_map_unit_with_base_unit():
    """
    Сценарий: Рекурсивная десериализация единицы измерения со встроенной базовой единицей
    Ожидаемый результат: Создаются связанные доменные модели unit_model, сохранен коэффициент ratio
    """
    # Подготовка
    base_dto = unit_dto(id="g-id", name="Грамм (г)", ratio=1.0, base_unit=None)
    kg_dto = unit_dto(id="kg-id", name="Килограмм (кг)", ratio=1000.0, base_unit=base_dto)
    factory = mapping_factory()

    # Действие
    kg_model = factory.map(kg_dto)

    # Проверка
    assert isinstance(kg_model, unit_model)
    assert kg_model.id == "kg-id"
    assert kg_model.name == "Килограмм (кг)"
    assert kg_model.ratio == 1000.0
    assert isinstance(kg_model.base_unit, unit_model)
    assert kg_model.base_unit.id == "g-id"
    assert kg_model.base_unit.name == "Грамм (г)"


def test_mapping_factory_map_nomenclature():
    """
    Сценарий: Десериализация номенклатуры с вложенной группой и единицей измерения
    Ожидаемый результат: Создается nomenclature_model с корректным enum-типом и связями
    """
    # Подготовка
    u_dto = unit_dto(id="g-id", name="Грамм (г)", ratio=1.0)
    g_dto = nomenclature_group_dto(id="raw-id", name="Сырье")
    n_dto = nomenclature_dto(
        id="sugar-id",
        name="Сахар",
        full_name="Сахар белый песок",
        group=g_dto,
        unit=u_dto,
        nom_type="Продукт"
    )
    factory = mapping_factory()

    # Действие
    nom_model = factory.map(n_dto)

    # Проверка
    assert isinstance(nom_model, nomenclature_model)
    assert nom_model.id == "sugar-id"
    assert nom_model.name == "Сахар"
    assert nom_model.full_name == "Сахар белый песок"
    assert nom_model.group.name == "Сырье"
    assert nom_model.unit.name == "Грамм (г)"
    assert nom_model.type == nomenclature_type.PRODUCT


def test_mapping_factory_identity_cache_uniqueness():
    """
    Сценарий: Повторная ссылка на одну и ту же сущность (одинаковый id) из разных объектов
    Ожидаемый результат: Кэш идентичности возвращает один и тот же экземпляр в памяти 
    """
    # Подготовка
    u_dto1 = unit_dto(id="same-unit-id", name="Грамм (г)", ratio=1.0)
    u_dto2 = unit_dto(id="same-unit-id", name="Грамм (г)", ratio=1.0)
    g_dto = nomenclature_group_dto(id="grp-id", name="Сырье")

    n1_dto = nomenclature_dto(id="n1", name="Сахар", full_name="Сахар", group=g_dto, unit=u_dto1)
    n2_dto = nomenclature_dto(id="n2", name="Соль", full_name="Соль", group=g_dto, unit=u_dto2)

    factory = mapping_factory()

    # Действие
    n1_model = factory.map(n1_dto)
    n2_model = factory.map(n2_dto)

    # Проверка
    assert n1_model.unit is n2_model.unit
    assert n1_model.group is n2_model.group


def test_mapping_factory_map_composite_recipe():
    """
    Сценарий: Десериализация составного рецепта, содержащего полуфабрикат со своим рецептом
    Ожидаемый результат: Рекурсивно собирается граф рецептов, полуфабрикат ссылается на подрецепт
    """
    # Подготовка
    factory = mapping_factory()
    u_dto = unit_dto(id="u1", name="Грамм (г)", ratio=1.0)
    g_dto = nomenclature_group_dto(id="g1", name="Полуфабрикаты")

    sauce_nom = nomenclature_dto(id="sauce-nom", name="Соус", full_name="Соус (п/ф)", group=g_dto, unit=u_dto, nom_type="Полуфабрикат")
    chicken_nom = nomenclature_dto(id="ch-nom", name="Курица", full_name="Курица", group=g_dto, unit=u_dto, nom_type="Продукт")

    sauce_ing = ingredient_dto(id="i1", name="Курица", gross_weight=100.0, net_weight=90.0, nomenclature=chicken_nom, unit=u_dto)
    sauce_recipe = recipe_dto(
        id="r-sauce",
        name="Рецепт соуса",
        portions=2,
        preparation_method="Варить",
        owner=sauce_nom,
        ingredients=[sauce_ing]
    )

    dish_nom = nomenclature_dto(id="dish-nom", name="Паста", full_name="Паста", group=g_dto, unit=u_dto, nom_type="Продукт")
    composite_ing = ingredient_dto(
        id="i2",
        name="Соус",
        gross_weight=50.0,
        net_weight=45.0,
        nomenclature=sauce_nom,
        unit=u_dto,
        recipe=sauce_recipe
    )
    main_recipe = recipe_dto(
        id="r-main",
        name="Рецепт пасты",
        portions=1,
        preparation_method="Собрать",
        owner=dish_nom,
        ingredients=[composite_ing]
    )

    # Действие
    main_model = factory.map(main_recipe)

    # Проверка
    assert isinstance(main_model, recipe_model)
    assert main_model.id == "r-main"
    assert len(main_model.ingredients) == 1

    ing = main_model.ingredients[0]
    assert ing.nomenclature.name == "Соус"
    assert ing.recipe is not None
    assert ing.recipe.id == "r-sauce"
    assert ing.recipe.name == "Рецепт соуса"


def test_mapping_factory_from_json_matches_storage_manager():
    """
    Сценарий: Поэлементное сравнение десериализованных моделей с эталоном storage_manager
    Ожидаемый результат: Все 5 коллекций совпадают по количеству, ID и атрибутам моделей
    """
    # Подготовка
    set_mgr = settings_manager()
    set_mgr.load()
    set_mgr.settings.is_first_start = True

    storage = storage_manager()
    storage.units.clear()
    storage.groups.clear()
    storage.warehouses.clear()
    storage.nomenclatures.clear()
    storage.recipes.clear()
    storage.load()

    # Действие: Сериализация и обратная десериализация
    conv_fact = convert_factory()
    json_text = conv_fact.to_json(storage.data)
    assert len(json_text) > 0

    map_fact = mapping_factory()
    loaded = map_fact.from_json(json_text)

    # Проверка:
    # Склады
    assert len(loaded["warehouse"]) == len(storage.warehouses)
    for orig, loaded_item in zip(storage.warehouses, loaded["warehouse"]):
        assert loaded_item.id == orig.id
        assert loaded_item.name == orig.name
        assert loaded_item.address == orig.address

    # Единицы измерения
    assert len(loaded["unit"]) == len(storage.units)
    for orig, loaded_item in zip(storage.units, loaded["unit"]):
        assert loaded_item.id == orig.id
        assert loaded_item.name == orig.name
        assert loaded_item.ratio == orig.ratio

    # Группы номенклатуры
    assert len(loaded["group"]) == len(storage.groups)
    for orig, loaded_item in zip(storage.groups, loaded["group"]):
        assert loaded_item.id == orig.id
        assert loaded_item.name == orig.name

    # Номенклатура
    assert len(loaded["nomenclature"]) == len(storage.nomenclatures)
    for orig, loaded_item in zip(storage.nomenclatures, loaded["nomenclature"]):
        assert loaded_item.id == orig.id
        assert loaded_item.name == orig.name
        assert loaded_item.full_name == orig.full_name
        assert loaded_item.type == orig.type
        assert loaded_item.group.name == orig.group.name
        assert loaded_item.unit.name == orig.unit.name

    # Рецепты
    assert len(loaded["recipe"]) == len(storage.recipes)
    for orig, loaded_item in zip(storage.recipes, loaded["recipe"]):
        assert loaded_item.id == orig.id
        assert loaded_item.name == orig.name
        assert loaded_item.portions == orig.portions
        assert loaded_item.owner.name == orig.owner.name
        assert len(loaded_item.ingredients) == len(orig.ingredients)


def test_mapping_factory_from_json_loads_storage_json_file():
    """
    Сценарий: Загрузка и десериализация исходного файла Json/storage.json
    Ожидаемый результат: Все 5 коллекций успешно восстанавливаются в доменные модели
    """
    # Подготовка
    path = os.path.join("Json", "storage.json")
    assert os.path.exists(path)

    with open(path, "r", encoding="utf-8") as f:
        json_text = f.read()

    factory = mapping_factory()

    # Действие
    loaded = factory.from_json(json_text)

    # Проверка
    assert len(loaded["warehouse"]) == 1
    assert len(loaded["unit"]) == 7
    assert len(loaded["group"]) == 5
    assert len(loaded["nomenclature"]) == 13
    assert len(loaded["recipe"]) == 2


def test_mapping_factory_from_json_empty_string_raises():
    """
    Сценарий: Передача пустой строки в метод from_json
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    factory = mapping_factory()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        factory.from_json("")


def test_mapping_factory_map_unsupported_type_raises():
    """
    Сценарий: Передача неподдерживаемого типа объекта в метод map
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    factory = mapping_factory()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        factory.map("произвольная_строка")

def test_models_create_from_dict():
    """
    Сценарий: Проверка фабричных методов create(data: dict) доменных моделей
    Ожидаемый результат: Модели создаются из словаря данных, сохраняя все переданные атрибуты и id
    """
    # Подготовка и Действие
    wh = warehouse_model.create({"id": "wh-1", "name": "Склад", "address": "Адрес"})
    grp = nomenclature_group_model.create({"id": "g-1", "name": "Сырье"})
    u = unit_model.create({"id": "u-1", "name": "Грамм (г)", "ratio": 1.0})
    nom = nomenclature_model.create(
        {"id": "n-1", "name": "Мука", "full_name": "Мука пшеничная"},
        group=grp,
        unit=u
    )
    ing = ingredient_model.create(
        {"id": "i-1", "net_weight": 100.0, "gross_weight": 110.0},
        nomenclature=nom,
        unit=u
    )
    rec = recipe_model.create(
        {"id": "r-1", "name": "Тесто", "portions": 2, "preparation_method": "Замесить"},
        owner=nom
    )

    # Проверка
    assert wh.id == "wh-1" and wh.name == "Склад" and wh.address == "Адрес"
    assert grp.id == "g-1" and grp.name == "Сырье"
    assert u.id == "u-1" and u.ratio == 1.0
    assert nom.id == "n-1" and nom.name == "Мука"
    assert ing.id == "i-1" and ing.net_weight == 100.0 and ing.gross_weight == 110.0
    assert rec.id == "r-1" and rec.portions == 2 and rec.owner == nom


def test_mapping_factory_independent_of_loading_order():
    """
    Сценарий: Обработка коллекций хранилища в обратном порядке (рецепты -> номенклатура -> группы -> единицы -> склады)
    Ожидаемый результат: Граф связей и ссылки успешно собираются без ошибок независимо от очередности
    """
    # Подготовка
    path = os.path.join("Json", "storage.json")
    with open(path, "r", encoding="utf-8") as f:
        import json
        data = json.loads(f.read())

    dto = storage_dto.from_dict(data)
    factory = mapping_factory()

    # Действие: Маппим коллекции в обратном порядке
    recipes = [factory.map_recipe(r) for r in dto.recipe if r]
    nomenclatures = [factory.map_nomenclature(n) for n in dto.nomenclature if n]
    groups = [factory.map_group(g) for g in dto.group if g]
    units = [factory.map_unit(u) for u in dto.unit if u]
    warehouses = [factory.map_warehouse(w) for w in dto.warehouse if w]

    # Проверка
    assert len(recipes) == 2
    assert len(nomenclatures) == 13
    assert len(units) == 7
    assert len(warehouses) == 1
    # Составной полуфабрикат соуса внутри пасты корректно связался с рецептом соуса
    assert recipes[1].ingredients[1].recipe is recipes[0]
    # Единица измерения у номенклатуры совпадает с закэшированной единицей
    assert recipes[1].ingredients[0].unit is units[0]