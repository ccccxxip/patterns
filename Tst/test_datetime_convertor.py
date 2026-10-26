import pytest
from datetime import datetime, date
from Src.Core.exception import arguments_exception
from Src.Logics.datetime_convertor import datetime_convertor


def test_datetime_convertor_datetime_success():
    """
    Сценарий: Конвертация объекта datetime в ISO-строку
    Ожидаемый результат: Возвращается словарь со строковым ISO-представлением даты и времени
    """
    # Подготовка
    conv = datetime_convertor()
    dt = datetime(2026, 10, 23, 10, 30, 0)

    # Действие
    result = conv.Convert(dt, field_name="created_at")

    # Проверка
    assert result == {"created_at": "2026-10-23T10:30:00"}


def test_datetime_convertor_date_success():
    """
    Сценарий: Конвертация объекта date в ISO-строку
    Ожидаемый результат: Возвращается словарь с датой в формате YYYY-MM-DD
    """
    # Подготовка
    conv = datetime_convertor()
    d = date(2026, 10, 23)

    # Действие
    result = conv.Convert(d)

    # Проверка
    assert result == {"value": "2026-10-23"}


def test_datetime_convertor_filters_dict():
    """
    Сценарий: Передача словаря со смешанными типами в datetime_convertor
    Ожидаемый результат: В словаре остаются только поля дат в формате ISO
    """
    # Подготовка
    conv = datetime_convertor()
    dt = datetime(2026, 10, 23, 12, 0, 0)
    data = {"created_at": dt, "count": 5, "name": "тест"}

    # Действие
    result = conv.Convert(data)

    # Проверка
    assert result == {"created_at": "2026-10-23T12:00:00"}


def test_datetime_convertor_none_raises():
    """
    Сценарий: Передача значения None в datetime_convertor
    Ожидаемый результат: Выбрасывается arguments_exception
    """
    # Подготовка
    conv = datetime_convertor()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        conv.Convert(None)


def test_datetime_convertor_invalid_primitive_raises():
    """
    Сценарий: Передача целочисленного значения вместо даты в datetime_convertor
    Ожидаемый результат: Выбрасывается arguments_exception с описанием неверного типа
    """
    # Подготовка
    conv = datetime_convertor()

    # Действие и Проверка
    with pytest.raises(arguments_exception):
        conv.Convert(12345)


def test_datetime_convertor_extracts_from_composite_object():
    """
    Сценарий: Извлечение полей даты из составного объекта со свойствами
    Ожидаемый результат: Из объекта извлекаются только поля даты
    """
    # Подготовка
    conv = datetime_convertor()

    class SampleEvent:
        @property
        def timestamp(self):
            return datetime(2026, 10, 24, 15, 0, 0)

        @property
        def title(self):
            return "Событие"

    event = SampleEvent()

    # Действие
    result = conv.Convert(event)

    # Проверка
    assert result == {"timestamp": "2026-10-24T15:00:00"}
