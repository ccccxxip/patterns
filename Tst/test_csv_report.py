import pytest
from Src.Logics.csv_report import csv_report
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


def test_csv_recipe_returns_binary():
    """
    Сценарий: формирование отчёта по рецепту в формате CSV
    Ожидаемый результат: отчёт возвращает двоичные данные (поле binary не пустое, text пустой)
    """
    # Подготовка
    report = csv_report()
    recipe = _create_test_recipe()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert isinstance(result, report_result_dto)
    assert len(result.binary) > 0
    assert result.text == ""


def test_csv_recipe_content():
    """
    Сценарий: проверка структуры и данных сформированного CSV-отчёта для рецепта
    Ожидаемый результат: файл содержит корректные заголовки таблицы, наименование ингредиента и строку итогов
    """
    # Подготовка
    report = csv_report()
    recipe = _create_test_recipe()

    # Действие
    result = report.build(recipe)
    content = bytes(result.binary).decode("utf-8-sig")

    # Проверка
    assert "Код;Наименование;Брутто (г);Нетто (г)" in content
    assert "Мука" in content
    assert "Итого Брутто" in content


def test_csv_nomenclature_content():
    """
    Сценарий: формирование отчёта по номенклатуре в формате CSV
    Ожидаемый результат: файл содержит строки с наименованиями полей и значениями свойств номенклатуры
    """
    # Подготовка
    report = csv_report()
    nom = _create_test_nomenclature()

    # Действие
    result = report.build(nom)
    content = bytes(result.binary).decode("utf-8-sig")

    # Проверка
    assert "Поле;Значение" in content
    assert "Сахар" in content
