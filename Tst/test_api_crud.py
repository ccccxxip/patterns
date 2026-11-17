import pytest
from starlette.testclient import TestClient
import main
from Src.Logics.storage_manager import storage_manager


@pytest.fixture
def client():
    """Фикстура тестового клиента API с предзагруженным хранилищем"""
    store = storage_manager()
    if not store.is_loaded:
        store.load()
    return TestClient(main.api)


def test_get_report_formats(client):
    """
    Сценарий: Получение списка всех доступных форматов генерации отчетов
    Ожидаемый результат: Статус 200, возвращается JSON-список из 5 форматов
    """
    # Подготовка
    expected_formats = {"TXT", "CSV", "MARKDOWN", "XML", "HTML"}

    # Действие
    response = client.get("/api/reports/formats")

    # Проверка
    assert response.status_code == 200
    formats = response.json()
    assert isinstance(formats, list)
    assert set(formats) == expected_formats


def test_get_report_formats_alias(client):
    """
    Сценарий: Получение списка форматов через альтернативный эндпоинт (алиас /api/get_report_formats)
    Ожидаемый результат: Статус 200, возвращается идентичный JSON-список из 5 форматов
    """
    # Подготовка
    expected_formats = {"TXT", "CSV", "MARKDOWN", "XML", "HTML"}

    # Действие
    response = client.get("/api/get_report_formats")

    # Проверка
    assert response.status_code == 200
    formats = response.json()
    assert isinstance(formats, list)
    assert set(formats) == expected_formats


def test_get_entities_keys(client):
    """
    Сценарий: Получение списка типов зарегистрированных доменных сущностей (/api/get_entities)
    Ожидаемый результат: Статус 200, возвращаются ключи доступных коллекций
    """
    # Подготовка
    expected_types = {"warehouse", "unit", "group", "nomenclature", "recipe"}

    # Действие
    response = client.get("/api/get_entities")

    # Проверка
    assert response.status_code == 200
    types = response.json()
    assert isinstance(types, list)
    assert expected_types.issubset(set(types))


def test_get_entities_list(client):
    """
    Сценарий: Получение списка сущностей типа 'warehouse'
    Ожидаемый результат: Статус 200, возвращается непустой список складов
    """
    # Подготовка
    endpoint = "/api/entities/warehouse"

    # Действие
    response = client.get(endpoint)

    # Проверка
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 1
    assert "address" in items[0]


def test_create_entity_success(client):
    """
    Сценарий: Создание новой сущности (склад) через POST-запрос
    Ожидаемый результат: Статус 201, сущность сохранена в хранилище с переданными полями
    """
    # Подготовка
    payload = {
        "id": "wh-new-test",
        "name": "Новый склад API",
        "address": "ул. Пушкина, 10"
    }

    try:
        # Действие
        response = client.post("/api/entities/warehouse", json=payload)

        # Проверка
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "wh-new-test"
        assert data["name"] == "Новый склад API"
        assert data["address"] == "ул. Пушкина, 10"
    finally:
        # Очистка
        client.delete("/api/entities/warehouse/wh-new-test")


def test_create_entity_duplicate_id_returns_400(client):
    """
    Сценарий: Попытка создания сущности с уже существующим ID
    Ожидаемый результат: Статус 400, ошибка о дубликате ID
    """
    # Подготовка
    payload = {
        "id": "wh-dup-test",
        "name": "Склад дубликат",
        "address": "ул. Первая, 1"
    }
    client.post("/api/entities/warehouse", json=payload)

    try:
        # Действие
        response = client.post("/api/entities/warehouse", json=payload)

        # Проверка
        assert response.status_code == 400
        assert "уже существует" in response.json().get("error", "")
    finally:
        # Очистка
        client.delete("/api/entities/warehouse/wh-dup-test")


def test_get_entity_by_id_success(client):
    """
    Сценарий: Получение конкретной сущности по уникальному ID
    Ожидаемый результат: Статус 200, возвращаются корректные данные сущности
    """
    # Подготовка
    payload = {
        "id": "wh-get-test",
        "name": "Склад для поиска",
        "address": "ул. Полевая, 5"
    }
    client.post("/api/entities/warehouse", json=payload)

    try:
        # Действие
        response = client.get("/api/entities/warehouse/wh-get-test")

        # Проверка
        assert response.status_code == 200
        assert response.json()["id"] == "wh-get-test"
        assert response.json()["name"] == "Склад для поиска"
    finally:
        # Очистка
        client.delete("/api/entities/warehouse/wh-get-test")


def test_get_nonexistent_entity_id_returns_404(client):
    """
    Сценарий: Запрос несуществующего ID сущности
    Ожидаемый результат: Статус 404 Not Found
    """
    # Подготовка
    non_existent_id = "unknown-id-99999"

    # Действие
    response = client.get(f"/api/entities/warehouse/{non_existent_id}")

    # Проверка
    assert response.status_code == 404
    assert "не найдена" in response.json().get("error", "")


def test_update_entity_success(client):
    """
    Сценарий: Обновление существующей сущности через PUT-запрос
    Ожидаемый результат: Статус 200, поля сущности обновлены
    """
    # Подготовка
    initial_payload = {
        "id": "wh-update-test",
        "name": "Склад старый",
        "address": "ул. Старая, 1"
    }
    client.post("/api/entities/warehouse", json=initial_payload)

    updated_payload = {
        "id": "wh-update-test",
        "name": "Склад обновленный",
        "address": "ул. Новая, 100"
    }

    try:
        # Действие
        response = client.put("/api/entities/warehouse/wh-update-test", json=updated_payload)

        # Проверка
        assert response.status_code == 200
        assert response.json()["name"] == "Склад обновленный"
        assert response.json()["address"] == "ул. Новая, 100"
    finally:
        # Очистка
        client.delete("/api/entities/warehouse/wh-update-test")


def test_patch_entity_partial_update_success(client):
    """
    Сценарий: Частичное обновление сущности через PATCH-запрос (меняется только имя, адрес сохраняется)
    Ожидаемый результат: Статус 200, имя обновлено, не переданные поля сохранены без изменений
    """
    # Подготовка
    initial_payload = {
        "id": "wh-patch-test",
        "name": "Склад до PATCH",
        "address": "ул. Неизменная, 42"
    }
    client.post("/api/entities/warehouse", json=initial_payload)

    patch_payload = {
        "name": "Склад после PATCH"
    }

    try:
        # Действие
        response = client.patch("/api/entities/warehouse/wh-patch-test", json=patch_payload)

        # Проверка
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Склад после PATCH"
        assert data["address"] == "ул. Неизменная, 42"
    finally:
        # Очистка
        client.delete("/api/entities/warehouse/wh-patch-test")


def test_delete_entity_success(client):
    """
    Сценарий: Успешное удаление изолированной сущности
    Ожидаемый результат: Статус 200, последующий GET возвращает 404
    """
    # Подготовка
    payload = {
        "id": "wh-delete-test",
        "name": "Склад под снос",
        "address": "ул. Временная, 7"
    }
    client.post("/api/entities/warehouse", json=payload)

    # Действие
    del_response = client.delete("/api/entities/warehouse/wh-delete-test")

    # Проверка
    assert del_response.status_code == 200
    assert del_response.json().get("result") == "success"

    verify_response = client.get("/api/entities/warehouse/wh-delete-test")
    assert verify_response.status_code == 404


def test_delete_referenced_unit_forbidden(client):
    """
    Сценарий: Попытка удаления связанной единицы измерения 'Грамм (г)',
    которая используется в номенклатуре и рецептах
    Ожидаемый результат: Статус 400, отказ в удалении (контроль целостности данных)
    """
    # Подготовка
    units_res = client.get("/api/entities/unit")
    gram_unit = next(u for u in units_res.json() if u["name"] == "Грамм (г)")

    # Действие
    del_res = client.delete(f"/api/entities/unit/{gram_unit['id']}")

    # Проверка
    assert del_res.status_code == 400
    error_msg = del_res.json().get("error", "")
    assert "Запрещено удалять" in error_msg
    assert "связана с другими объектами" in error_msg


def test_delete_referenced_group_forbidden(client):
    """
    Сценарий: Попытка удаления группы номенклатуры 'Ингредиенты',
    в которую входят зарегистрированные товары
    Ожидаемый результат: Статус 400, отказ в удалении (Domain Invariant)
    """
    # Подготовка
    groups_res = client.get("/api/entities/group")
    ing_group = next(g for g in groups_res.json() if g["name"] == "Ингредиенты")

    # Действие
    del_res = client.delete(f"/api/entities/group/{ing_group['id']}")

    # Проверка
    assert del_res.status_code == 400
    error_msg = del_res.json().get("error", "")
    assert "Запрещено удалять" in error_msg
    assert "связана с другими объектами" in error_msg


def test_update_referenced_entity_id_forbidden(client):
    """
    Сценарий: Попытка изменить уникальный код (id) у связанной единицы измерения
    Ожидаемый результат: Статус 400, отказ в изменении ID связанного объекта
    """
    # Подготовка
    units_res = client.get("/api/entities/unit")
    gram_unit = next(u for u in units_res.json() if u["name"] == "Грамм (г)")
    upd_payload = {
        "id": "new-forbidden-id",
        "name": "Грамм переименованный",
        "ratio": 1.0
    }

    # Действие
    put_res = client.put(f"/api/entities/unit/{gram_unit['id']}", json=upd_payload)

    # Проверка
    assert put_res.status_code == 400
    error_msg = put_res.json().get("error", "")
    assert "Запрещено изменять код (id)" in error_msg