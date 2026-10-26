import pytest
from Src.Core.exception import arguments_exception
from Src.Logics.reference_convertor import reference_convertor
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model


def test_reference_convertor_unit_model_success():
    """
    Сценарий: Конвертация доменной сущности (unit_model)
    Ожидаемый результат: Возвращается словарь ссылочного представления {'id': ..., 'name': ...}
    """
    # Подготовка
    conv = reference_convertor()
    unit = unit_model("кг", 1000.0)

    # Действие
    result = conv.Convert(unit)

    # Проверка
    assert result == {"id": unit.id, "name": "кг"}


def test_reference_convertor_with_custom_field_name():
    """
    Сценарий: Конвертация сущности с указанием имени поля field_name
    Ожидаемый результат: Результат оборачивается в {field_name: {"id": ..., "name": ...}}
    """
    # Подготовка
    conv = reference_convertor()
    unit = unit_model("кг", 1000.0)

    # Действие
    result = conv.Convert(unit, field_name="unit")

    # Проверка
    assert result == {"unit": {"id": unit.id, "name": "кг"}}


def test_reference_convertor_extracts_references_from_composite_model():
    """
    Сценарий: Конвертация составной номенклатуры (поля-ссылки group и unit)
    Ожидаемый результат: Извлекаются только поля-ссылки group и unit в виде словарей {id, name}, простые поля не включаются
    """
    # Подготовка
    conv = reference_convertor()
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create_product("Сахар", "Сахар-песок", raw, g)

    # Действие
    result = conv.Convert(nom)

    # Проверка
    assert "group" in result
    assert result["group"] == {"id": raw.id, "name": raw.name}
    assert "unit" in result
    assert result["unit"] == {"id": g.id, "name": g.name}
    assert "full_name" not in result


def test_reference_convertor_filters_dict():
    """
    Сценарий: Передача словаря со смешанными типами
    Ожидаемый результат: В словаре остаются только поля-ссылки в виде словарей {id, name}
    """
    # Подготовка
    conv = reference_convertor()
    raw = nomenclature_group_model.create_raw()
    data = {"group": raw, "title": "текст", "count": 100}

    # Действие
    result = conv.Convert(data)

    # Проверка
    assert result == {"group": {"id": raw.id, "name": raw.name}}


def test_reference_convertor_none_raises():
    """
    Сценарий: Передача значения None
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    conv = reference_convertor()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        conv.Convert(None)


def test_reference_convertor_invalid_type_raises():
    """
    Сценарий: Передача не ссылочного типа (строки)
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    conv = reference_convertor()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        conv.Convert("строка_не_ссылка")
