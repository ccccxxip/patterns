import pytest
import json
import tempfile
import os
from Src.Logics.settings_manager import settings_manager
from Src.Core.exception import arguments_exception
from Src.Core.validator import operation_exception


def test_not_raise_settings_manager_load():
    """
    Проверка, что метод load() отрабатывает без выброса исключений 
    при загрузке настроек по умолчанию
    """
    # Подготовка
    manager = settings_manager()
    is_exception = False
    
    # Действие
    try:
        manager.load()
    except Exception:
        is_exception = True
        
    # Проверка
    assert is_exception is False


def test_not_empty_settings_manager_load():
    """
    Проверка, что после загрузки настроек модель settings не пустая
    """
    # Подготовка
    manager = settings_manager()
    
    # Действие
    manager.load()
    
    # Проверка
    assert manager.settings is not None


def test_equals_settings_manager_create():
    """
    Проверка работы паттерна Singleton: два созданных экземпляра 
    менеджера должны являться одним и тем же объектом
    """
    # Подготовка / Действие
    instance1 = settings_manager()
    instance2 = settings_manager()
    
    # Проверка
    assert instance1 is not None
    assert instance2 is not None
    assert instance1 == instance2


def test_is_loaded_settings_manager_true():
    """
    Проверка, что флаг is_loaded устанавливается в True после успешного вызова load()
    """
    # Подготовка
    manager = settings_manager()
    
    # Действие
    manager.load()
    
    # Проверка
    assert manager.is_loaded is True


def test_same_settings_in_different_instances():
    """
    Проверка, что у разных экземпляров менеджера (Singleton) 
    настройки ссылаются на одни и те же данные
    """
    # Подготовка
    instance1 = settings_manager()
    instance2 = settings_manager()
    
    # Действие
    instance1.load()
    
    # Проверка
    assert instance1.settings is not None
    assert instance2.settings is not None
    assert instance1.settings == instance2.settings


def test_settings_manager_load_populates_organization_from_json():
    """
    Проверка, что при корректной загрузке JSON 
    данные организации успешно парсятся и сохраняются в модели
    """
    # Подготовка
    manager = settings_manager()
    
    # Действие
    manager.load()
    organization = manager.settings.organization

    # Проверка
    assert organization is not None
    assert organization.name == "ООО Ромашка"
    assert organization.inn == "7701234567"


def test_settings_manager_load_with_incomplete_organization_raises_operation_exception():
    """
    Проверка, что загрузка файла с неполными данными об организации 
    перехватывается и вызывает исключение operation_exception
    """
    # Подготовка
    broken_data = {
        "organization": {
            "name": "ООО Ромашка",
            "inn": "7701234567"
        },
        "is_first_start": True,
        "boss_name": "Иванов И.И.",
        "account_name": "Основной расчетный счет",
    }

    # Создаем временный файл с кривым JSON
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(broken_data, tmp_file, ensure_ascii=False)
        tmp_path = tmp_file.name

    manager = settings_manager()
    is_exception = False

    # Действие
    try:
        manager.load(tmp_path)
    except operation_exception:
        is_exception = True
    finally:
        # Убираем временный файл 
        os.remove(tmp_path)

    # Проверка
    assert is_exception is True