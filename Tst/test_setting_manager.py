import pytest
from Src.Logics.setting_manager import settings_manager
from Src.Core.exception import arguments_exception


def test_not_raise_settings_manager_load():
    manager = settings_manager()
    try:
        manager.load()
    except Exception as e:
        pytest.fail(f"Метод load() вызвал исключение: {e}")


def test_not_empty_settings_manager_load():
    manager = settings_manager()
    manager.load()
    assert manager.settings is not None


def test_equals_settings_manager_create():
    instance1 = settings_manager()
    instance2 = settings_manager()
    assert instance1 is not None
    assert instance2 is not None
    assert instance1 == instance2


def test_is_loaded_settings_manager_true():
    manager = settings_manager()
    manager.load()
    assert manager.is_loaded is True


def test_same_settings_in_different_instances():
    instance1 = settings_manager()
    instance2 = settings_manager()
    instance1.load()
    assert instance1.settings is not None
    assert instance2.settings is not None
    assert instance1.settings == instance2.settings