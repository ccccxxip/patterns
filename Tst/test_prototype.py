import pytest
from Src.Logics.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_item_dto import filter_item_dto
from Src.Core.filter_type import filter_type
from Src.Logics.storage_manager import storage_manager


@pytest.fixture
def storage():
    """Фикстура хранилища с инициализированными данными"""
    sm = storage_manager()
    if not sm.is_loaded:
        sm.load()
    return sm


def test_prototype_clone_empty_or_none_filter(storage):
    """
    Сценарий: Клонирование прототипа без фильтра или с пустым фильтром
    Ожидаемый результат: Возвращается новый объект прототипа с идентичным набором данных
    """
    # Подготовка
    units = storage.get_entities_by_type("unit")
    proto = prototype(units)
    empty_dto = filter_dto()

    # Действие
    cloned = proto.clone()
    cloned_empty = proto.clone(empty_dto)

    # Проверка
    assert isinstance(cloned, prototype)
    assert cloned is not proto
    assert len(cloned.data) == len(units)
    assert len(cloned_empty.data) == len(units)


def test_prototype_filter_unit_by_name_equals(storage):
    """
    Сценарий: Фильтрация единиц измерения по точному названию (EQUALS)
    Ожидаемый результат: Находится ровно одна единица измерения
    """
    # Подготовка
    units = storage.get_entities_by_type("unit")
    proto = prototype(units)
    f = filter_dto()
    f.name = "Килограмм (кг)"
    f.filter_type = filter_type.EQUALS

    # Действие
    result = proto.clone(f)

    # Проверка
    assert len(result.data) == 1
    assert result.data[0].name == "Килограмм (кг)"


def test_prototype_filter_unit_by_name_like(storage):
    """
    Сценарий: Фильтрация единиц измерения по части названия (LIKE)
    Ожидаемый результат: Находятся все ложки (чайная, столовая)
    """
    # Подготовка
    units = storage.get_entities_by_type("unit")
    proto = prototype(units)
    f = filter_dto()
    f.name = "ложка"
    f.filter_type = filter_type.LIKE

    # Действие
    result = proto.clone(f)

    # Проверка
    assert len(result.data) >= 2
    for item in result.data:
        assert "ложка" in item.name.lower()


def test_prototype_filter_by_id_equals(storage):
    """
    Сценарий: Фильтрация сущностей по id
    Ожидаемый результат: Находится сущность с соответствующим id
    """
    # Подготовка
    groups = storage.get_entities_by_type("group")
    target_group = groups[0]
    proto = prototype(groups)
    f = filter_dto()
    f.id = target_group.id
    f.filter_type = filter_type.EQUALS

    # Действие
    result = proto.clone(f)

    # Проверка
    assert len(result.data) == 1
    assert result.data[0].id == target_group.id


def test_prototype_nested_unit_search_by_base_unit(storage):
    """
    Сценарий: Поиск производной единицы измерения через её базовую единицу (вложенная структура)
    Ожидаемый результат: Поиск 'Грамм' находит как сам грамм, так и производные единицы (кг, ч.л.)
    """
    # Подготовка
    units = storage.get_entities_by_type("unit")
    proto = prototype(units)
    f = filter_dto()
    f.name = "Грамм (г)"
    f.filter_type = filter_type.EQUALS

    # Действие
    result = proto.clone(f)

    # Проверка
    names = [u.name for u in result.data]
    assert "Грамм (г)" in names
    assert "Килограмм (кг)" in names


def test_prototype_nested_nomenclature_by_group(storage):
    """
    Сценарий: Фильтрация номенклатуры по наименованию её группы (вложенная структура)
    Ожидаемый результат: При поиске группы 'Сырье' возвращаются номенклатуры, входящие в эту группу
    """
    # Подготовка
    nomenclatures = storage.get_entities_by_type("nomenclature")
    proto = prototype(nomenclatures)
    f = filter_dto()
    f.name = "Сырье"
    f.filter_type = filter_type.EQUALS

    # Действие
    result = proto.clone(f)

    # Проверка
    assert len(result.data) > 0
    for nom in result.data:
        assert nom.group is not None
        assert nom.group.name == "Сырье"


def test_prototype_nested_recipe_by_ingredient(storage):
    """
    Сценарий: Поиск рецептов по номенклатуре ингредиента (глубокая вложенная структура)
    Ожидаемый результат: Поиск номенклатуры ингредиента находит содержащие его рецепты
    """
    # Подготовка
    recipes = storage.get_entities_by_type("recipe")
    proto = prototype(recipes)
    f = filter_dto()
    f.name = "Чеснок"
    f.filter_type = filter_type.LIKE

    # Действие
    result = proto.clone(f)

    # Проверка
    assert len(result.data) > 0
    names = [r.name for r in result.data]
    assert "Приготовление соуса" in names


def test_prototype_method_chaining(storage):
    """
    Сценарий: Каскадная фильтрация через вызов .clone(f1).clone(f2)
    Ожидаемый результат: Последовательное применение двух фильтров возвращает пересечение условий
    """
    # Подготовка
    units = storage.get_entities_by_type("unit")
    proto = prototype(units)
    f1 = filter_dto()
    f1.name = "Грамм"
    f1.filter_type = filter_type.LIKE
    f2 = filter_dto()
    f2.name = "Кило"
    f2.filter_type = filter_type.LIKE

    # Действие
    result = proto.clone(f1).clone(f2)

    # Проверка
    assert len(result.data) == 1
    assert result.data[0].name == "Килограмм (кг)"


def test_contains_data_prototype_transactions(storage):
    """
    Сценарий: Проверка фильтрации транзакций через прототип
    Ожидаемый результат: Возвращаются отфильтрованные транзакции номенклатуры
    """
    # Подготовка
    transactions = storage.get_entities_by_type("transaction")
    pr = prototype(transactions)
    f = filter_dto()
    f.name = "Куриное филе"
    f.filter_type = filter_type.EQUALS

    # Действие
    result = pr.clone(f)

    # Проверка
    assert len(result.data) > 0
    for t in result.data:
        assert t.nomenclature.name == "Куриное филе"
        assert t.value != 0


def test_contains_data_prototype_teacher_syntax(storage):
    """
    Сценарий: Проверка фильтрации
    Ожидаемый результат: Возвращаются отфильтрованные транзакции номенклатуры
    """
    # Подготовка
    f = filter_dto()
    item = filter_item_dto()
    item.field_name = "name"
    item.filter_type = "eq"
    item.value = "Куриное филе"
    f.filters = [item]
    pr = prototype(storage.data[storage_manager.transaction_key()])

    # Действие
    result = pr.clone(f)

    # Проверка
    assert len(result.data) > 0
    for t in result.data:
        assert t.nomenclature.name == "Куриное филе"


def test_prototype_filter_both_name_and_id_conjunction(storage):
    """
    Сценарий: Фильтрация сущностей при одновременном указании name и id в одном filter_dto
    Ожидаемый результат: Применяется логическое И — возвращается только сущность, у которой совпадают оба поля
    """
    # Подготовка
    warehouses = storage.get_entities_by_type("warehouse")
    target_wh = warehouses[0]
    proto = prototype(warehouses)

    f_match = filter_dto()
    f_match.name = target_wh.name
    f_match.id = target_wh.id
    f_match.filter_type = filter_type.EQUALS

    f_mismatch = filter_dto()
    f_mismatch.name = target_wh.name
    f_mismatch.id = "non-existent-id"
    f_mismatch.filter_type = filter_type.EQUALS

    # Действие
    result_match = proto.clone(f_match)
    result_mismatch = proto.clone(f_mismatch)

    # Проверка
    assert len(result_match.data) == 1
    assert result_match.data[0].id == target_wh.id
    assert len(result_mismatch.data) == 0
