import pytest
import json
import tempfile
import os
from Src.Logics.settings_manager import settings_manager


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
    Проверка работы Singleton: два созданных экземпляра 
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


def test_settings_manager_load_with_incomplete_organization_sets_is_loaded_false():
    """
    Проверка, что загрузка неполных данных об организации не вызывает исключение,
    а переводит флаг is_loaded в False
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

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(broken_data, tmp_file, ensure_ascii=False)
        tmp_path = tmp_file.name

    if hasattr(settings_manager, "instance"):
        del settings_manager.instance

    manager = settings_manager()

    # Действие
    try:
        manager.load(tmp_path)
    finally:
        os.remove(tmp_path)

    # Проверка
    assert manager.is_loaded is False
    assert manager.settings.organization is None
    assert manager.settings.boss_name == "Иванов И.И."


def test_settings_manager_load_with_missing_inn_key_sets_is_loaded_false():
    """
    Проверка конкретного сценария: отсутствие ключа 'inn' не ломает программу,
    а устанавливает is_loaded в False
    """
    # Подготовка
    broken_data = {
        "organization": {
            "name": "ООО Ромашка",
            "bik": "044525225",
            "account": "40702810938000012345",
            "ownership_form": "ООО",
        },
        "is_first_start": True,
        "boss_name": "Иванов И.И.",
        "account_name": "Основной расчетный счет",
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(broken_data, tmp_file, ensure_ascii=False)
        tmp_path = tmp_file.name

    if hasattr(settings_manager, "instance"):
        del settings_manager.instance

    manager = settings_manager()

    # Действие
    try:
        manager.load(tmp_path)
    finally:
        os.remove(tmp_path)

    # Проверка
    assert manager.is_loaded is False
    assert manager.settings.organization is None


def test_settings_manager_load_with_organization_as_wrong_type_sets_is_loaded_false():
    """
    Проверка, что передача строки вместо словаря в блоке organization
    безопасно обрабатывается менеджером
    """
    # Подготовка
    broken_data = {
        "organization": "это не словарь",
        "is_first_start": True,
        "boss_name": "Иванов И.И.",
        "account_name": "Основной расчетный счет",
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(broken_data, tmp_file, ensure_ascii=False)
        tmp_path = tmp_file.name

    if hasattr(settings_manager, "instance"):
        del settings_manager.instance

    manager = settings_manager()
    is_exception = False

    # Действие
    try:
        manager.load(tmp_path)
    except Exception:
        is_exception = True
    finally:
        os.remove(tmp_path)

    # Проверка
    assert is_exception is False
    assert manager.is_loaded is False