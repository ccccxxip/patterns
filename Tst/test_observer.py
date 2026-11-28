import os
import inspect
import pytest
from Src.Core.abstract_observer import abstract_observer
from Src.Core.event_type import event_type
from Src.Core.exception import arguments_exception
from Src.Logics.observer import observer
from Src.Logics.log_observer import log_observer
from Src.Core.constants import LOG_ENCODING


class dummy_observer(abstract_observer):
    """Тестовый наблюдатель для проверки механизма оповещения"""

    def __init__(self):
        self.received_events = []

    def handler(self, event_types: str, params: object = None) -> None:
        self.received_events.append((event_types, params))


@pytest.fixture(autouse=True)
def clean_observer_handlers():
    """Очистка списка обработчиков до и после каждого теста"""
    observer.clear()
    yield
    observer.clear()


def test_abstract_observer_cannot_be_instantiated():
    """
    Сценарий: Попытка создания экземпляра абстрактного класса abstract_observer
    Ожидаемый результат: Класс является абстрактным, создание экземпляра вызывает TypeError
    """
    # Подготовка и Проверка: класс является абстрактным
    assert inspect.isabstract(abstract_observer) is True

    # Действие и Проверка: попытка создания вызывает TypeError
    with pytest.raises(TypeError):
        globals()["abstract_observer"]()


def test_event_type_constants():
    """
    Сценарий: Проверка возвращаемых значений типов событий event_type
    Ожидаемый результат: Все методы возвращают ожидаемые строковые идентификаторы, класс является Enum
    """
    # Подготовка, Действие, Проверка
    from enum import Enum
    assert issubclass(event_type, Enum)
    assert event_type.CREATE_ENTITY == "create_entity"
    assert event_type.load_settings() == "load_settings"
    assert event_type.change_settings() == "change_settings"
    assert event_type.create_entity() == "create_entity"
    assert event_type.update_entity() == "update_entity"
    assert event_type.delete_entity() == "delete_entity"
    assert event_type.warehouse_transaction() == "warehouse_transaction"
    assert event_type.api_request() == "api_request"


def test_observer_add_and_create_notifies_handler():
    """
    Сценарий: Регистрация наблюдателя и вызов события через observer.create
    Ожидаемый результат: Зарегистрированный наблюдатель получает переданное событие
    """
    # Подготовка
    obs = dummy_observer()
    observer.add(obs)

    # Действие
    observer.create(event_type.create_entity(), "Тестовая сущность")

    # Проверка
    assert len(obs.received_events) == 1
    event_name, params = obs.received_events[0]
    assert event_name == "create_entity"
    assert params == "Тестовая сущность"


def test_observer_prevents_duplicate_registration():
    """
    Сценарий: Повторная регистрация одного и того же объекта наблюдателя
    Ожидаемый результат: Наблюдатель добавляется в список только один раз
    """
    # Подготовка
    obs = dummy_observer()
    observer.add(obs)
    observer.add(obs)

    # Действие
    observer.create(event_type.load_settings())

    # Проверка
    assert len(obs.received_events) == 1


def test_observer_delete_removes_handler():
    """
    Сценарий: Удаление зарегистрированного наблюдателя
    Ожидаемый результат: После удаления наблюдатель перестает получать уведомления
    """
    # Подготовка
    obs = dummy_observer()
    observer.add(obs)
    observer.delete(obs)

    # Действие
    observer.create(event_type.change_settings())

    # Проверка
    assert len(obs.received_events) == 0


def test_observer_add_invalid_type_raises():
    """
    Сценарий: Передача некорректного типа в observer.add
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    invalid_source = "not_an_observer"

    # Действие, Проверка
    with pytest.raises(arguments_exception):
        observer.add(invalid_source)


def test_log_observer_writes_to_file(tmp_path):
    """
    Сценарий: Запись события в файл через log_observer
    Ожидаемый результат: В указанном файле появляется форматированная строка события
    """
    # Подготовка
    log_file = tmp_path / "test_logs" / "test.log"
    logger = log_observer(str(log_file))
    observer.add(logger)

    # Действие
    observer.create(event_type.warehouse_transaction(), "Поступление товара 50 кг")

    # Проверка
    assert os.path.exists(str(log_file))
    with open(str(log_file), "r", encoding=LOG_ENCODING) as f:
        content = f.read()

    assert "[WAREHOUSE_TRANSACTION]" in content
    assert "Поступление товара 50 кг" in content


def test_log_observer_equality_and_duplicate_prevention():
    """
    Сценарий: Проверка равенства двух log_observer с одинаковым файлом и защита от дубликатов
    Ожидаемый результат: Логгеры с одним файлом равны, в observer добавляется только один
    """
    # Подготовка
    l1 = log_observer("Logs/app.log")
    l2 = log_observer("Logs/app.log")
    l3 = log_observer("Logs/other.log")

    # Действие
    observer.add(l1)
    observer.add(l2)

    # Проверка
    assert l1 == l2
    assert l1 != l3
    assert len(observer.handlers) == 1
