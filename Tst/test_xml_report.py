import pytest
from Src.Logics.xml_report import xml_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Models.recipe_model import recipe_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model


def _create_test_recipe() -> recipe_model:
    """Вспомогательный метод: создаёт тестовый рецепт с ингредиентом"""
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    dish = nomenclature_model.create_product("Блинчики", "Блинчики", raw, g)
    flour = nomenclature_model.create_product("Мука", "Мука пшеничная", raw, g)
    recipe = recipe_model("Блинчики", dish, preparation_method="Жарить", portions=2)
    recipe.add_ingredient(ingredient_model(flour, 140.0, 150.0, g))
    return recipe


def _create_test_nomenclature() -> nomenclature_model:
    """Вспомогательный метод: создаёт тестовую номенклатуру"""
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    return nomenclature_model.create_product("Сахар", "Сахар-песок", raw, g)


def test_xml_recipe_returns_text():
    """
    Сценарий: формирование отчёта по рецепту в формате XML
    Ожидаемый результат: отчёт возвращает структурированный текст (поле text заполнено, binary пустое)
    """
    # Подготовка
    report = xml_report()
    recipe = _create_test_recipe()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert isinstance(result, report_result_dto)
    assert len(result.text) > 0
    assert result.binary == []


def test_xml_recipe_content():
    """
    Сценарий: проверка корректности структуры XML-дерева рецепта
    Ожидаемый результат: строка содержит XML-декларацию, тег <recipe>, элементы ингредиентов и итоги
    """
    # Подготовка
    report = xml_report()
    recipe = _create_test_recipe()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert '<?xml version="1.0"' in result.text
    assert "<recipe>" in result.text
    assert "<name>Мука</name>" in result.text
    assert "<total_gross>150.00</total_gross>" in result.text


def test_xml_nomenclature_content():
    """
    Сценарий: формирование XML-отчёта по карточке номенклатуры
    Ожидаемый результат: формируется валидный XML-документ с корневым тегом <nomenclature>
    """
    # Подготовка
    report = xml_report()
    nom = _create_test_nomenclature()

    # Действие
    result = report.build(nom)

    # Проверка
    assert "<nomenclature>" in result.text
    assert "<name>Сахар</name>" in result.text
