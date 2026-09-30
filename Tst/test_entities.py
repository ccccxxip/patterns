from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.constants import NAME_MAX_LENGTH


class test_entity(base_model):
    """Класс для проверки работы базовой модели"""
    pass


def test_base_model_get_id_not_null():
    """
    Сценарий: создаем новый объект и проверяем его id
    Ожидаемый результат: id создается сразу и он не пустой
    """
    entity = test_entity()
    assert entity.id != ""


def test_base_model_unique_id_for_different_instances():
    """
    Сценарий: создаем два разных объекта
    Ожидаемый результат: у каждого объекта свой уникальный id, они не совпадают
    """
    entity1 = test_entity()
    entity2 = test_entity()
    assert entity1.id != entity2.id


def test_entities_with_same_id_are_equal():
    """
    Сценарий: сравниваем два объекта с одинаковыми id
    Ожидаемый результат: объекты должны быть равны, т.к. сравниваем по id
    """
    entity1 = test_entity()
    entity2 = test_entity()

    entity1.id = "12345"
    entity2.id = "12345"

    assert entity1 == entity2


def test_name_setter_empty_string_raises_arguments_exception():
    """
    Сценарий: пытаемся передать пустую строку или пробелы в наименование
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    entity = test_entity()
    is_exception = False

    try:
        entity.name = "   "
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_name_setter_invalid_type_raises_arguments_exception():
    """
    Сценарий: передаем не строковое значение (число) в наименование
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    entity = test_entity()
    is_exception = False

    try:
        entity.name = 123
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_name_setter_long_name_raises_arguments_exception():
    """
    Сценарий: передаем наименование длиннее 50 символов (больше NAME_MAX_LENGTH)
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    entity = test_entity()
    is_exception = False
    long_name = "А" * (NAME_MAX_LENGTH + 1)

    try:
        entity.name = long_name
    except arguments_exception:
        is_exception = True

    assert is_exception is True