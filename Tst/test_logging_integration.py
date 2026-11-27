import pytest
from starlette.testclient import TestClient
from Src.Core.abstract_observer import abstract_observer
from Src.Core.event_type import event_type
from Src.Core.constants import TRANSACTION_KEY
from Src.Logics.observer import observer
from Src.Logics.storage_manager import storage_manager
from Src.Logics.settings_manager import settings_manager
from Src.Models.unit_model import unit_model
from Src.Models.settings_model import settings_model
from main import api


class capturing_observer(abstract_observer):
    """Наблюдатель, собирающий все события для верификации в тестах"""

    def __init__(self):
        self.events = []

    def handler(self, event_types: str, params: object = None) -> None:
        self.events.append((event_types, params))


@pytest.fixture
def capture():
    """Фикстура для перехвата событий Наблюдателя"""
    obs = capturing_observer()
    observer.add(obs)
    yield obs
    observer.delete(obs)


def test_logging_settings_load_and_change(capture):
    """
    Сценарий: Логирование загрузки и изменения настроек системы
    Ожидаемый результат: Перехватываются события load_settings и change_settings
    """
    # Подготовка
    sm = settings_manager()

    # Действие
    sm.load()
    load_events = [e for e in capture.events if e[0] == event_type.load_settings()]

    new_s = settings_model()
    new_s.organization_name = "Новая организация"
    sm.update_settings(new_s)
    change_events = [e for e in capture.events if e[0] == event_type.change_settings()]

    # Проверка
    assert len(load_events) >= 1
    assert len(change_events) >= 1
    assert "Настройки обновлены" in change_events[0][1]


def test_logging_storage_crud_operations(capture):
    """
    Сценарий: Логирование CRUD операций в хранилище (создание, обновление, удаление)
    Ожидаемый результат: Фиксируются события create_entity, update_entity, delete_entity
    """
    # Подготовка
    storage = storage_manager()
    u = unit_model("Тестовая штука", 1)
    u.id = "test-unit-id-for-crud-log"

    # Действие
    storage.add_entity("unit", u)
    create_events = [e for e in capture.events if e[0] == event_type.create_entity() and "test-unit-id-for-crud-log" in str(e[1])]

    u_updated = unit_model("Обновленная штука", 1)
    u_updated.id = "test-unit-id-for-crud-log"
    storage.update_entity("unit", "test-unit-id-for-crud-log", u_updated)
    update_events = [e for e in capture.events if e[0] == event_type.update_entity() and "test-unit-id-for-crud-log" in str(e[1])]

    storage.delete_entity("unit", "test-unit-id-for-crud-log")
    delete_events = [e for e in capture.events if e[0] == event_type.delete_entity() and "test-unit-id-for-crud-log" in str(e[1])]

    # Проверка
    assert len(create_events) == 1
    assert len(update_events) == 1
    assert len(delete_events) == 1


def test_logging_warehouse_transaction(capture):
    """
    Сценарий: Логирование складской операции (движения номенклатуры)
    Ожидаемый результат: Фиксируется событие warehouse_transaction
    """
    # Подготовка
    storage = storage_manager()
    wh = storage.get_entities_by_type("warehouse")[0]
    nom = storage.get_entities_by_type("nomenclature")[0]
    from Src.Models.transaction_model import transaction_model
    from datetime import datetime

    tx = transaction_model.create_receipt(wh, nom, nom.unit, 42.5, datetime.now())

    # Действие
    storage.add(TRANSACTION_KEY, tx)
    tx_events = [e for e in capture.events if e[0] == event_type.warehouse_transaction()]

    # Проверка
    assert len(tx_events) >= 1
    assert any("42.5" in str(e[1]) for e in tx_events)


def test_logging_web_api_requests(capture):
    """
    Сценарий: Логирование вызовов Web-методов API
    Ожидаемый результат: Фиксируется событие api_request с методом и путем запроса
    """
    # Подготовка
    client = TestClient(api)

    # Действие
    response = client.get("/api/reports/formats")

    # Проверка
    assert response.status_code == 200
    web_events = [e for e in capture.events if e[0] == event_type.api_request()]
    assert len(web_events) >= 1
    assert any("GET /api/reports/formats" in str(e[1]) for e in web_events)
