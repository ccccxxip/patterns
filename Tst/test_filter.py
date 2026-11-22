from Src.Core.filter_type import filter_type
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.filter_item_dto import filter_item_dto
from Src.Logics.mapping_factory import mapping_factory
from Src.Core.common import common


def test_filter_type_enum_values():
    """
    Сценарий: Проверка допустимых значений перечисления filter_type
    Ожидаемый результат: Присутствуют режимы EQUALS и LIKE
    """
    # Подготовка
    expected_equals = "EQUALS"
    expected_like = "LIKE"

    # Действие
    actual_equals = filter_type.EQUALS.value
    actual_like = filter_type.LIKE.value

    # Проверка
    assert actual_equals == expected_equals
    assert actual_like == expected_like


def test_filter_type_match_equals():
    """
    Сценарий: Проверка функции filter_type.match в режиме EQUALS
    Ожидаемый результат: Совпадение только при полном равенстве без учета регистра и пробелов
    """
    # Подготовка
    source = "  Мука пшеничная "
    query = "мука пшеничная"

    # Действие
    result = filter_type.match(source, query, filter_type.EQUALS)

    # Проверка
    assert result is True
    assert filter_type.match("Сахар белый", "сахар", filter_type.EQUALS) is False
    assert filter_type.match("Любая строка", "", filter_type.EQUALS) is True


def test_filter_type_match_like():
    """
    Сценарий: Проверка функции filter_type.match в режиме LIKE
    Ожидаемый результат: Совпадение при частичном вхождении подстроки
    """
    # Подготовка
    source = "Мука пшеничная высший сорт"
    query = "мука"

    # Действие
    result = filter_type.match(source, query, filter_type.LIKE)

    # Проверка
    assert result is True
    assert filter_type.match("Соль поваренная", "сахар", filter_type.LIKE) is False


def test_filter_dto_properties_and_docstrings():
    """
    Сценарий: Проверка инкапсуляции, геттеров, сеттеров и docstring в filter_dto
    Ожидаемый результат: Свойства содержат описания, сеттеры нормализуют значения
    """
    # Подготовка
    dto = filter_dto()

    # Действие
    dto.name = "  Тестовое имя  "
    dto.id = "  id-123  "
    dto.filter_type = "LIKE"

    # Проверка
    assert filter_dto.name.__doc__ is not None
    assert filter_dto.id.__doc__ is not None
    assert filter_dto.filter_type.__doc__ is not None
    assert dto.name == "Тестовое имя"
    assert dto.id == "id-123"
    assert dto.filter_type == filter_type.LIKE
    assert dto.is_empty is False


def test_filter_dto_from_dict_reflection():
    """
    Сценарий: Создание filter_dto из словаря через рефлексию
    Ожидаемый результат: Объект создается через common.get_fields
    """
    # Подготовка
    data = {
        "name": "Мука",
        "id": "item-01",
        "filter_type": "LIKE"
    }

    # Действие
    dto = filter_dto.from_dict(data)

    # Проверка
    assert dto is not None
    assert dto.name == "Мука"
    assert dto.id == "item-01"
    assert dto.filter_type == filter_type.LIKE


def test_filter_dto_empty_flags():
    """
    Сценарий: Проверка флага is_empty для пустого filter_dto
    Ожидаемый результат: is_empty равен True при пустых полях
    """
    # Подготовка
    dto = filter_dto()

    # Проверка до заполнения
    assert dto.is_empty is True

    # Действие
    dto.name = "Сахар"

    # Проверка после заполнения
    assert dto.is_empty is False


def test_mapping_factory_deserializes_filter_dto():
    """
    Сценарий: Десериализация filter_dto через единую точку mapping_factory
    Ожидаемый результат: Возвращается провалидированный объект filter_dto
    """
    # Подготовка
    factory = mapping_factory()
    data = {
        "name": "Соль",
        "filter_type": "EQUALS"
    }

    # Действие
    result = factory.deserialize("filter", data)

    # Проверка
    assert isinstance(result, filter_dto)
    assert result.name == "Соль"
    assert result.filter_type == filter_type.EQUALS


def test_filter_dto_supports_teacher_item_format():
    """
    Сценарий: Проверка поддержки формата filter_item_dto
    Ожидаемый результат: Корректно устанавливаются значения через filter_item_dto
    """
    # Подготовка
    f = filter_dto()
    item = filter_item_dto()
    item.field_name = "name"
    item.filter_type = "eq"
    item.value = "Килограмм"

    # Действие
    f.filters = [item]

    # Проверка
    assert len(f.filters) == 1
    assert f.filters[0].field_name == "name"
    assert f.filters[0].value == "Килограмм"
    assert f.filters[0].filter_type == filter_type.EQUALS


def test_filter_dto_from_dict_with_nested_filters():
    """
    Сценарий: Создание filter_dto из словаря с вложенными словарями filters
    Ожидаемый результат: Вложенные словари автоматически превращаются в filter_item_dto
    """
    # Подготовка
    data = {
        "filters": [
            {"field_name": "name", "value": "Мука", "filter_type": "LIKE"}
        ]
    }

    # Действие
    dto = filter_dto.from_dict(data)

    # Проверка
    assert dto is not None
    assert len(dto.filters) == 1
    assert isinstance(dto.filters[0], filter_item_dto)
    assert dto.filters[0].field_name == "name"
    assert dto.filters[0].value == "Мука"
    assert dto.filters[0].filter_type == filter_type.LIKE


def test_filter_type_match_string_mode():
    """
    Сценарий: Проверка функции filter_type.match при передаче режима строкой
    Ожидаемый результат: Метод корректно распознает строковые значения режима
    """
    # Подготовка
    source = "Мука пшеничная"
    query = "мука"

    # Действие
    result = filter_type.match(source, query, "LIKE")

    # Проверка
    assert result is True


def test_filter_dto_from_dict_with_is_empty_field():
    """
    Сценарий: Создание filter_dto из словаря, содержащего поле is_empty
    Ожидаемый результат: Рефлексия отрабатывает без исключений
    """
    # Подготовка
    data = {
        "name": "Мука",
        "is_empty": False
    }

    # Действие
    dto = filter_dto.from_dict(data)

    # Проверка
    assert dto is not None
    assert dto.name == "Мука"
    assert dto.is_empty is False



def test_filter_type_match_string_mode():
    """
    Сценарий: Проверка функции filter_type.match при передаче режима строкой
    Ожидаемый результат: Метод корректно распознает строковые значения режима
    """
    # Подготовка
    source = "Мука пшеничная"
    query = "мука"

    # Действие
    result = filter_type.match(source, query, "LIKE")

    # Проверка
    assert result is True


def test_filter_dto_from_dict_with_is_empty_field():
    """
    Сценарий: Создание filter_dto из словаря, содержащего поле is_empty
    Ожидаемый результат: Рефлексия отрабатывает без исключений
    """
    # Подготовка
    data = {
        "name": "Мука",
        "is_empty": False
    }

    # Действие
    dto = filter_dto.from_dict(data)

    # Проверка
    assert dto is not None
    assert dto.name == "Мука"
    assert dto.is_empty is False