import pytest
from Src.Core.exception import arguments_exception
from Src.Logics.basic_convertor import basic_convertor
from Src.Models.nomenclature_group_model import nomenclature_group_model


def test_basic_convertor_numeric_success():
    """
    Сценарий: Конвертация int, float
    Ожидаемый результат: Возвращается словарь формата {'value': <значение>}
    """
    # Подготовка
    conv = basic_convertor()

    # Действие
    res_int = conv.Convert(42)
    res_float = conv.Convert(3.14)

    # Проверка
    assert res_int == {"value": 42}
    assert res_float == {"value": 3.14}


def test_basic_convertor_str_with_custom_field_name():
    """
    Сценарий: Конвертация строки с передачей явного имени поля field_name
    Ожидаемый результат: Возвращается словарь с указанным ключом {'title': 'Тест'}
    """
    # Подготовка
    conv = basic_convertor()

    # Действие
    result = conv.Convert("Тест", field_name="title")

    # Проверка
    assert result == {"title": "Тест"}


def test_basic_convertor_bool_success():
    """
    Сценарий: Конвертация bool
    Ожидаемый результат: Возвращается словарь формата {'value': True/False}
    """
    # Подготовка
    conv = basic_convertor()

    # Действие
    res_true = conv.Convert(True)
    res_false = conv.Convert(False)

    # Проверка
    assert res_true == {"value": True}
    assert res_false == {"value": False}


def test_basic_convertor_extracts_scalar_fields_from_model():
    """
    Сценарий: Извлечение скалярных полей (строк/чисел) из составной модели
    Ожидаемый результат: Возвращаются только простые поля модели (id, name), без сложных связей
    """
    # Подготовка
    conv = basic_convertor()
    group = nomenclature_group_model.create_raw()

    # Действие
    result = conv.Convert(group)

    # Проверка
    assert "id" in result
    assert result["name"] == group.name


def test_basic_convertor_filters_dict():
    """
    Сценарий: Передача словаря со смешанными типами
    Ожидаемый результат: В возвращаемом словаре остаются только простые типы (числа, строки, bool)
    """
    # Подготовка
    conv = basic_convertor()
    group = nomenclature_group_model.create_raw()
    data = {"count": 10, "label": "штуки", "is_active": True, "ref": group}

    # Действие
    result = conv.Convert(data)

    # Проверка
    assert result == {"count": 10, "label": "штуки", "is_active": True}


def test_basic_convertor_none_raises():
    """
    Сценарий: Передача значения None
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    conv = basic_convertor()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        conv.Convert(None)
