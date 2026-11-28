import datetime
from Src.Models.log_model import log_model
from Src.Core.log_subsystem import log_subsystem
from Src.Dtos.log_type_enum import log_type_enum
from Src.Core.event_type import event_type


def test_log_model_creation_and_properties():
    """
    Сценарий: Создание объекта log_model и проверка его свойств
    Ожидаемый результат: Все свойства корректно сохраняют переданные значения
    """
    # Подготовка
    now = datetime.datetime.now()

    # Действие
    log = log_model(
        subsystem=log_subsystem.STORAGE,
        level=log_type_enum.INFO,
        event=event_type.warehouse_transaction(),
        message="Тестовая складская операция",
        period=now
    )

    # Проверка
    assert log.subsystem == log_subsystem.STORAGE
    assert log.level == log_type_enum.INFO
    assert log.event == event_type.WAREHOUSE_TRANSACTION
    assert log.message == "Тестовая складская операция"
    assert log.period == now
    assert "Тестовая складская операция" in log


def test_log_model_str_formatting():
    """
    Сценарий: Проверка строкового форматирования записи лога
    Ожидаемый результат: Строка содержит уровень, подсистему, событие и сообщение []
    """
    # Подготовка
    log = log_model(
        subsystem=log_subsystem.CRUD,
        level=log_type_enum.ERROR,
        event=event_type.delete_entity(),
        message="Запрещено удалять сущность"
    )

    # Действие
    result = str(log)

    # Проверка
    assert "[ERROR]" in result
    assert "[CRUD]" in result
    assert "[DELETE_ENTITY]" in result
    assert "Запрещено удалять сущность" in result


def test_log_type_enum_values():
    """
    Сценарий: Проверка перечисления log_type_enum
    Ожидаемый результат: Перечисление содержит уровни DEBUG, INFO, ERROR
    """
    # Подготовка, Действие, Проверка
    assert log_type_enum.DEBUG == "DEBUG"
    assert log_type_enum.INFO == "INFO"
    assert log_type_enum.ERROR == "ERROR"


def test_log_subsystem_values():
    """
    Сценарий: Проверка перечисления log_subsystem
    Ожидаемый результат: Перечисление содержит подсистемы Settings, Storage, CRUD, Web, System
    """
    # Подготовка, Действие, Проверка
    assert log_subsystem.SETTINGS == "Settings"
    assert log_subsystem.STORAGE == "Storage"
    assert log_subsystem.CRUD == "CRUD"
    assert log_subsystem.WEB == "Web"
    assert log_subsystem.SYSTEM == "System"
