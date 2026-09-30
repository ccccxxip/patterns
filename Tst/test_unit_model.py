from Src.Core.exception import arguments_exception
from Src.Models.unit_model import unit_model


def test_create_base_unit_returns_object_with_self_base_unit():
    """
    Сценарий: создание основной единицы измерения, у которой нет базовой
    Ожидаемый результат: базовая единица ссылается на этот же объект
    """
    unit = unit_model("грамм", 1)

    assert unit.name == "грамм"
    assert unit.ratio == 1.0
    assert unit.base_unit == unit


def test_create_derived_unit_returns_object_with_correct_base_unit():
    """
    Сценарий: создание зависимой единицы (килограмм со ссылкой на грамм)
    Ожидаемый результат: объект правильно привязывает базовую единицу
    """
    base = unit_model("грамм", 1)
    derived = unit_model("кг", 1000, base)

    assert derived.name == "кг"
    assert derived.ratio == 1000.0
    assert derived.base_unit == base


def test_to_base_calculates_correct_value():
    """
    Сценарий: проверка пересчета значений в базовую единицу через метод to_base
    Ожидаемый результат: 2.5 кг правильно пересчитываются в 2500 грамм
    """
    base = unit_model("грамм", 1)
    derived = unit_model("кг", 1000, base)

    assert derived.to_base(2.5) == 2500.0


def test_ratio_zero_raises_arguments_exception():
    """
    Сценарий: передача 0 в качестве коэффициента пересчета
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False

    try:
        unit_model("кг", 0)
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_ratio_negative_raises_arguments_exception():
    """
    Сценарий: передача отрицательного коэффициента пересчета
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False

    try:
        unit_model("кг", -100)
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_invalid_base_unit_type_raises_arguments_exception():
    """
    Сценарий: передача строки вместо объекта unit_model в качестве базовой единицы
    Ожидаемый результат: выбрасывается исключение из-за неверного типа данных
    """
    is_exception = False

    try:
        unit_model("кг", 1000, base_unit="не объект unit_model")
    except arguments_exception:
        is_exception = True

    assert is_exception is True