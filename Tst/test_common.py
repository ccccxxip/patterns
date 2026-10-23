import pytest
from Src.Core.common import common
from Src.Core.exception import arguments_exception
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.recipe_model import recipe_model
from Src.Models.ingredient_model import ingredient_model
from Src.Logics.csv_report import csv_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.html_report import html_report
from Src.Logics.xml_report import xml_report
from Src.Logics.text_report import text_report
from Src.Core.abstract_report_factory import abstract_factory
from Src.Dtos.report_result_dto import report_result_dto


def test_common_get_fields_none_raises():
    """
    Сценарий: передача пустого значения (None) в метод get_fields модуля common
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    # Подготовка
    is_exception = False

    # Действие
    try:
        common.get_fields(None)
    except arguments_exception:
        is_exception = True

    # Проверка
    assert is_exception is True


def test_common_get_fields_nomenclature():
    """
    Сценарий: получение списка публичных свойств номенклатуры через рефлексию
    Ожидаемый результат: список содержит все свойства модели и не содержит приватных атрибутов
    """
    # Подготовка
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create_product("Сахар", "Сахар-песок", raw, g)

    # Действие
    fields = common.get_fields(nom)

    # Проверка
    assert "id" in fields
    assert "name" in fields
    assert "full_name" in fields
    assert "group" in fields
    assert "unit" in fields
    assert "type" in fields
    assert not any(f.startswith("_") for f in fields)


def test_common_get_fields_recipe_filter_lists():
    """
    Сценарий: фильтрация коллекций и списков флагом is_common=True для сложной модели
    Ожидаемый результат: при is_common=True списки исключаются, при is_common=False присутствуют
    """
    # Подготовка
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    dish = nomenclature_model.create_product("Блинчики", "Блинчики", raw, g)
    flour = nomenclature_model.create_product("Мука", "Мука пшеничная", raw, g)
    recipe = recipe_model("Блинчики", dish, portions=2)
    recipe.add_ingredient(ingredient_model(flour, 140.0, 150.0, g))

    # Действие
    scalar_fields = common.get_fields(recipe, is_common=True)
    all_fields = common.get_fields(recipe, is_common=False)

    # Проверка
    assert "ingredients" not in scalar_fields
    assert "ingredients" in all_fields
    assert "name" in scalar_fields
    assert "id" in scalar_fields


def test_reports_metadata():
    """
    Сценарий: проверка метаданных отчётов на соответствие принципам SOLID
    Ожидаемый результат: каждый класс отчёта декларирует валидные mime_type, file_extension и флаг is_attachment
    """
    # Подготовка
    reports = [
        (csv_report(), "text/csv", "csv", True),
        (markdown_report(), "text/markdown", "md", True),
        (html_report(), "text/html", "html", False),
        (xml_report(), "application/xml", "xml", False),
        (text_report(), "text/plain", "txt", False),
    ]

    # Действие и Проверка
    for report, expected_mime, expected_ext, expected_attach in reports:
        assert report.mime_type == expected_mime
        assert report.file_extension == expected_ext
        assert report.is_attachment == expected_attach


def test_abstract_factory_declares_create_default():
    """
    Сценарий: проверка объявления метода create_default в абстрактном интерфейсе
    Ожидаемый результат: класс abstract_factory содержит объявление абстрактного метода create_default
    """
    # Подготовка и Проверка
    assert hasattr(abstract_factory, "create_default")

def test_common_get_field_title_from_docstrings():
    """
    Сценарий: извлечение названий полей из docstrings свойств через рефлексию
    Ожидаемый результат: метод common.get_field_title возвращает корректные наименования из @property.__doc__
    """
    # Действие и Проверка: извлечение наименований из docstrings
    assert common.get_field_title(nomenclature_model, "name") == "Наименование"
    assert common.get_field_title(nomenclature_model, "id") == "Код"
    assert common.get_field_title(nomenclature_model, "full_name") == "Полное наименование"
    assert common.get_field_title(recipe_model, "portions") == "Порций"
    assert common.get_field_title(recipe_model, "total_gross_weight") == "Итого Брутто"
    # Для неизвестного поля возвращается отформатированное имя
    assert common.get_field_title(nomenclature_model, "unknown_field") == "Unknown field"

def test_abstract_report_register_custom_handler():
    """
    Сценарий: динамическая регистрация специализированного обработчика типа в abstract_report
    Ожидаемый результат: метод build вызывает зарегистрированный через register обработчик,
    а незарегистрированные типы обрабатываются через _build_generic
    """
    # Подготовка
    report = text_report()
    called = []

    def custom_handler(src):
        called.append(src)
        result = report_result_dto()
        result.text = f"CUSTOM: {src.name}"
        return result

    # Регистрируем специализированный обработчик для номенклатуры
    report.register(nomenclature_model, custom_handler)
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create_product("Сахар", "Сахар-песок", raw, g)

    # Действие 1: вызов для зарегистрированного типа
    result_nom = report.build(nom)

    # Проверка 1: сработал зарегистрированный обработчик
    assert len(called) == 1
    assert called[0] is nom
    assert result_nom.text == "CUSTOM: Сахар"

    # Действие и Проверка 2: незарегистрированный тип (unit_model) идёт через стандартный _build_generic
    unit = unit_model.create_gram()
    result_unit = report.build(unit)
    assert "Единица измерения" in result_unit.text


