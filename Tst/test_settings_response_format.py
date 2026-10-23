import pytest
from Src.Models.settings_model import settings_model
from Src.Logics.settings_manager import settings_manager
from Src.Dtos.report_type_dto import report_type_enum
from Src.Core.exception import arguments_exception


def test_settings_model_default_format():
    """
    Проверка, что значение по умолчанию для response_format в модели настроек — TXT
    """
    # Подготовка / Действие
    model = settings_model()

    # Проверка
    assert model.response_format == report_type_enum.TXT


def test_settings_model_set_valid_format():
    """
    Проверка успешной установки корректного значения response_format в settings_model
    """
    # Подготовка
    model = settings_model()

    # Действие
    model.response_format = report_type_enum.MARKDOWN

    # Проверка
    assert model.response_format == report_type_enum.MARKDOWN

    # Проверяем также другие типы
    model.response_format = report_type_enum.CSV
    assert model.response_format == report_type_enum.CSV

    model.response_format = report_type_enum.XML
    assert model.response_format == report_type_enum.XML

    model.response_format = report_type_enum.HTML
    assert model.response_format == report_type_enum.HTML


def test_settings_model_set_invalid_format_raises():
    """
    Проверка, что передача значения некорректного типа вызывает arguments_exception
    """
    # Подготовка
    model = settings_model()
    is_exception = False

    # Действие
    try:
        # Передаём строку вместо объекта enum
        model.response_format = "MARKDOWN"
    except arguments_exception:
        is_exception = True

    # Проверка
    assert is_exception is True


def test_settings_manager_loads_response_format_from_file():
    """
    Проверка, что settings_manager корректно читает response_format из settings.json
    """
    # Подготовка
    manager = settings_manager()

    # Действие
    manager.load()

    # Проверка (в Src/settings.json задано значение "MARKDOWN")
    assert manager.settings.response_format == report_type_enum.MARKDOWN
