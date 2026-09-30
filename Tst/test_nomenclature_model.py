from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model
from Src.Core.constants import FULL_NAME_MAX_LENGTH
from Src.Core.exception import arguments_exception


def _make_group() -> nomenclature_group_model:
    """Быстрое создание группы для тестов"""
    return nomenclature_group_model("Молочные продукты")


def _make_unit() -> unit_model:
    """Быстрое создание единицы измерения для тестов"""
    return unit_model("кг", 1.0)


def test_create_nomenclature_with_valid_data_returns_object():
    """
    Сценарий: создание номенклатуры с корректными полями
    Ожидаемый результат: объект создается, все свойства сохраняются без изменений
    """
    group = _make_group()
    unit = _make_unit()

    item = nomenclature_model("Молоко", "Молоко пастеризованное 3.2%", group, unit)

    assert item.name == "Молоко"
    assert item.full_name == "Молоко пастеризованное 3.2%"
    assert item.group is group
    assert item.unit is unit


def test_create_nomenclature_with_full_name_over_255_chars_raises_arguments_exception():
    """
    Сценарий: передача полного наименования длиннее 255 символов
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False
    group = _make_group()
    unit = _make_unit()
    full_name_256 = "б" * (FULL_NAME_MAX_LENGTH + 1)

    try:
        nomenclature_model("Товар", full_name_256, group, unit)
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_create_nomenclature_with_invalid_group_type_raises_arguments_exception():
    """
    Сценарий: передача строки вместо объекта группы номенклатуры
    Ожидаемый результат: конструктор выбрасывает arguments_exception
    """
    is_exception = False
    unit = _make_unit()

    try:
        nomenclature_model("Товар", "Полное наименование товара", "не группа", unit)
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_create_nomenclature_with_invalid_unit_type_raises_arguments_exception():
    """
    Сценарий: передача строки вместо объекта единицы измерения
    Ожидаемый результат: конструктор выбрасывает arguments_exception
    """
    is_exception = False
    group = _make_group()

    try:
        nomenclature_model("Товар", "Полное наименование товара", group, "не единица измерения")
    except arguments_exception:
        is_exception = True

    assert is_exception is True