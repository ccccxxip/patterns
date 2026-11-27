import pytest
from starlette.testclient import TestClient
import main
from Src.Logics.storage_manager import storage_manager


@pytest.fixture
def client():
    """Фикстура тестового клиента API с инициализированным хранилищем"""
    store = storage_manager()
    if not store.is_loaded:
        store.load()
    return TestClient(main.api)


def test_api_filter_entities_by_name_like(client):
    """
    Сценарий: Фильтрация единиц измерения через POST /api/filter/unit в режиме LIKE
    Ожидаемый результат: Статус 200, возвращается список найденных ложек
    """
    # Подготовка
    payload = {
        "name": "ложка",
        "filter_type": "LIKE"
    }

    # Действие
    response = client.post("/api/filter/unit", json=payload)

    # Проверка
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 2
    for item in items:
        assert "ложка" in item["name"].lower()


def test_api_filter_entities_by_name_equals(client):
    """
    Сценарий: Фильтрация номенклатуры через POST /api/filter/nomenclature в режиме EQUALS
    Ожидаемый результат: Статус 200, возвращается ровно одна позиция
    """
    # Подготовка
    payload = {
        "name": "Куриное филе",
        "filter_type": "EQUALS"
    }

    # Действие
    response = client.post("/api/filter/nomenclature", json=payload)

    # Проверка
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["name"] == "Куриное филе"


def test_api_filter_entities_nested_structure(client):
    """
    Сценарий: Фильтрация номенклатуры по наименованию её группы (поиск по вложенным структурам)
    Ожидаемый результат: Статус 200, возвращаются номенклатуры, входящие в группу 'Сырье'
    """
    # Подготовка
    payload = {
        "name": "Сырье",
        "filter_type": "EQUALS"
    }

    # Действие
    response = client.post("/api/filter/nomenclature", json=payload)

    # Проверка
    assert response.status_code == 200
    items = response.json()
    assert len(items) > 0


def test_api_filter_entities_unknown_type_returns_400(client):
    """
    Сценарий: Запрос фильтрации для несуществующего типа сущности
    Ожидаемый результат: Статус 400 с сообщением об ошибке
    """
    # Подготовка
    payload = {"name": "test"}

    # Действие
    response = client.post("/api/filter/unknown_entity", json=payload)

    # Проверка
    assert response.status_code == 400
    assert "Неизвестный тип сущности" in response.json()["error"]


def test_api_osv_report_without_filter(client):
    """
    Сценарий: Запрос полной оборотно-сальдовой ведомости через POST /api/reports/osv
    Ожидаемый результат: Статус 200, возвращается ведомость со всеми строками номенклатуры
    """
    # Подготовка
    payload = {}

    # Действие
    response = client.post("/api/reports/osv", json=payload)

    # Проверка
    assert response.status_code == 200
    rows = response.json()
    assert isinstance(rows, list)
    assert len(rows) > 0
    assert "start_balance" in rows[0]
    assert "end_balance" in rows[0]


def test_api_osv_report_with_filter(client):
    """
    Сценарий: Запрос ОСВ с фильтрацией по номенклатуре через Прототип
    Ожидаемый результат: Статус 200, возвращается строка ведомости только для искомой номенклатуры
    """
    # Подготовка
    payload = {
        "name": "Чеснок",
        "filter_type": "EQUALS"
    }

    # Действие
    response = client.post("/api/reports/osv", json=payload)

    # Проверка
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 1
    assert rows[0]["nomenclature"]["name"] == "Чеснок"