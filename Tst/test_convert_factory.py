import pytest
from datetime import datetime
from Src.Core.exception import arguments_exception
from Src.Logics.convert_factory import convert_factory
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model
from Src.Models.ingredient_model import ingredient_model
from Src.Logics.storage_manager import storage_manager
import os


def test_convert_factory_create_returns_correct_convertors():
    """
    Сценарий: Проверка фабричного метода create для различных типов данных и строковых ключей
    Ожидаемый результат: Фабрика возвращает соответствующие спец конвертеры
    """
    # Подготовка
    factory = convert_factory()

    # Действие и Проверка
    assert isinstance(factory.create(int), basic_convertor)
    assert isinstance(factory.create(str), basic_convertor)
    assert isinstance(factory.create(datetime), datetime_convertor)
    assert isinstance(factory.create(unit_model), reference_convertor)
    assert isinstance(factory.create("basic"), basic_convertor)
    assert isinstance(factory.create("datetime"), datetime_convertor)
    assert isinstance(factory.create("reference"), reference_convertor)


def test_convert_factory_create_none_raises():
    """
    Сценарий: Передача None в фабричный метод create
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    factory = convert_factory()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        factory.create(None)


def test_convert_factory_create_unsupported_type_raises():
    """
    Сценарий: Запрос конвертера для неизвестного типа данных через метод create
    Ожидаемый результат: Выбрасывается arguments_exception с описанием неподдерживаемого типа
    """
    # Подготовка
    factory = convert_factory()

    class UnknownCustomType:
        pass

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        factory.create(UnknownCustomType)


def test_convert_factory_convert_primitives_and_datetime():
    """
    Сценарий: Конвертация примитивных типов и даты через метод Convert фабрики
    Ожидаемый результат: Значения сериализуются в скалярные типы и ISO-строки
    """
    # Подготовка
    factory = convert_factory()
    dt = datetime(2026, 10, 23, 15, 0, 0)

    # Действие
    res_str = factory.Convert("Привет")
    res_num = factory.Convert(100)
    res_dt = factory.Convert(dt)

    # Проверка
    assert res_str == "Привет"
    assert res_num == 100
    assert res_dt == "2026-10-23T15:00:00"


def test_convert_factory_convert_none_returns_none():
    """
    Сценарий: Передача значения None в метод Convert фабрики
    Ожидаемый результат: Возвращается None
    """
    # Подготовка
    factory = convert_factory()

    # Действие и Проверка
    assert factory.Convert(None) is None


def test_convert_factory_convert_composite_nomenclature_model():
    """
    Сценарий: Конвертация сложной доменной модели nomenclature_model с вложенными ссылками (group и unit)
    Ожидаемый результат: Формируется словарь, где свойства group и unit сериализованы
    """
    # Подготовка
    factory = convert_factory()
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    nom = nomenclature_model.create_product("Мука", "Мука высший сорт", raw, g)

    # Действие
    result = factory.Convert(nom)

    # Проверка
    assert isinstance(result, dict)
    assert result["name"] == "Мука"
    assert result["full_name"] == "Мука высший сорт"
    assert isinstance(result["group"], dict)
    assert result["group"]["name"] == "Сырье"
    assert isinstance(result["unit"], dict)
    assert result["unit"]["name"] == "Грамм (г)"


def test_convert_factory_convert_recipe_model_with_ingredients():
    """
    Сценарий: Конвертация технологической карты с вложенным списком ингредиентов
    Ожидаемый результат: Все вложенные ингредиенты, владелец и числовые веса корректно конвертируются в словари
    """
    # Подготовка
    factory = convert_factory()
    g = unit_model.create_gram()
    raw = nomenclature_group_model.create_raw()
    sugar = nomenclature_model.create_product("Сахар", "Сахар-песок", raw, g)
    dish = nomenclature_model.create_product("Сироп", "Сахарный сироп", raw, g)

    recipe = recipe_model("Сироп рецепт", dish, portions=2)
    ing = ingredient_model(sugar, 95.0, 100.0, g)
    recipe.add_ingredient(ing)

    # Действие
    result = factory.Convert(recipe)

    # Проверка
    assert isinstance(result, dict)
    assert result["name"] == "Сироп рецепт"
    assert result["portions"] == 2
    assert result["owner"]["name"] == "Сироп"
    assert isinstance(result["ingredients"], list)
    assert len(result["ingredients"]) == 1
    assert result["ingredients"][0]["nomenclature"]["name"] == "Сахар"
    assert result["ingredients"][0]["gross_weight"] == 100.0
    assert result["ingredients"][0]["net_weight"] == 95.0


def test_convert_factory_convert_list_of_models():
    """
    Сценарий: Сериализация списка доменных моделей
    Ожидаемый результат: Возвращается список словарей
    """
    # Подготовка
    factory = convert_factory()
    g = unit_model.create_gram()
    kg = unit_model("Килограмм", 1000.0, g)

    # Действие
    result = factory.Convert([g, kg])

    # Проверка
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Грамм (г)"
    assert result[1]["name"] == "Килограмм"


def test_convert_factory_to_json():
    """
    Сценарий: Сериализация объекта в JSON-строку через метод to_json
    Ожидаемый результат: Получена корректная JSON-строка
    """
    # Подготовка
    factory = convert_factory()
    g = unit_model.create_gram()

    # Действие
    json_str = factory.to_json(g)

    # Проверка
    assert isinstance(json_str, str)
    assert '"name": "Грамм (г)"' in json_str
    assert '"id":' in json_str


def test_export_storage_data_to_json_files():
    """
    Сценарий: Проверка экспорта всех коллекций хранилища данных в файлы JSON
    Ожидаемый результат: Все 5 коллекций успешно сериализуются в JSON-файлы
    """
    # Подготовка
    storage = storage_manager()
    storage.convert()
    factory = convert_factory()

    collections = {
        "groups.json": storage.data["group"],
        "nomenclature.json": storage.data["nomenclature"],
        "recipes.json": storage.data["recipe"],
        "units.json": storage.data["unit"],
        "warehouses.json": storage.data["warehouse"]
    }

    # Действие и Проверка
    for file_name, items in collections.items():
        json_text = factory.to_json(items)
        assert len(json_text) > 0
        path = os.path.join("Json", file_name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(json_text)
        assert os.path.exists(path)
