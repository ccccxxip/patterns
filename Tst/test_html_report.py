import pytest
from Src.Logics.html_report import html_report
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


def test_html_recipe_returns_text():
    """
    Сценарий: формирование отчёта по рецепту в формате HTML
    Ожидаемый результат: отчёт возвращает текстовые данные в поле text
    """
    # Подготовка
    report = html_report()
    recipe = _create_test_recipe()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert isinstance(result, report_result_dto)
    assert len(result.text) > 0
    assert result.binary == []


def test_html_recipe_content():
    """
    Сценарий: проверка разметки сформированного HTML-отчёта для рецепта
    Ожидаемый результат: сформирован HTML-документ со стилями, таблицей состава и строкой итогов
    """
    # Подготовка
    report = html_report()
    recipe = _create_test_recipe()

    # Действие
    result = report.build(recipe)

    # Проверка
    assert "<!DOCTYPE html>" in result.text
    assert "<table>" in result.text
    assert "Мука" in result.text
    assert "Итого Брутто" in result.text


def test_html_nomenclature_content():
    """
    Сценарий: формирование HTML-отчёта по карточке номенклатуры
    Ожидаемый результат: сформирована HTML-страница с заголовком номенклатуры и метаданными
    """
    # Подготовка
    report = html_report()
    nom = _create_test_nomenclature()

    # Действие
    result = report.build(nom)

    # Проверка
    assert "<!DOCTYPE html>" in result.text
    assert "<h1>Номенклатура: Сахар</h1>" in result.text
