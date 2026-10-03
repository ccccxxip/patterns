import pytest
from Src.Logics.settings_manager import settings_manager
from Src.Core.exception import arguments_exception


def test_not_raise_settings_manager_load():
    """ 
    Сценарий: вызов метода load() без передачи аргументов
    Ожидаемый результат: метод подхватывает путь по умолчанию и не вызывает исключений
    """
    # Подготовка: создаем экземпляр менеджера настроек
    manager = settings_manager()
    
    # Действие и Проверка: 
    # Пытаемся загрузить данные 
    # Если возникает ошибка, тест перехватывает её и принудительно завершается с ошибкой
    try:
        manager.load()
    except Exception as e:
        pytest.fail(f"Метод load() вызвал исключение: {e}")


def test_not_empty_settings_manager_load():
    """ 
    Сценарий: успешная загрузка файла настроек
    Ожидаемый результат: свойство settings заполняется данными и перестает быть пустым
    """
    # Подготовка: создаем экземпляр менеджера
    manager = settings_manager()
    
    # Действие: вызываем загрузку данных из файла
    manager.load()
    
    # Проверка: утверждаем, что коробка с настройками успешно заполнилась
    assert manager.settings is not None


def test_equals_settings_manager_create():
    """ 
    Сценарий: многократное создание settings_manager
    Ожидаемый результат: благодаря Singleton всегда возвращается один и тот же объект в памяти
    """
    # Подготовка и Действие: пытаемся создать два независимых экземпляра
    instance1 = settings_manager()
    instance2 = settings_manager()
    
    # Проверка: убеждаемся, что оба существуют, и утверждаем, что это один и тот же объект
    assert instance1 is not None
    assert instance2 is not None
    assert instance1 == instance2


def test_is_loaded_settings_manager_true():
    """ 
    Сценарий: успешная загрузка данных менеджером
    Ожидаемый результат: флаг is_loaded переключается в True
    """
    # Подготовка: создаем экземпляр менеджера
    manager = settings_manager()
    
    # Действие: загружаем данные
    manager.load()
    
    # Проверка: утверждаем, что флаг успешной загрузки активен
    assert manager.is_loaded is True


def test_same_settings_in_different_instances():
    """ 
    Сценарий: загрузка данных через один экземпляр Singleton и проверка через другой
    Ожидаемый результат: данные автоматически доступны во всех экземплярах, тк объект общий
    """
    # Подготовка: получаем две ссылки на менеджер
    instance1 = settings_manager()
    instance2 = settings_manager()
    
    # Действие: загружаем настройки через первый экземпляр
    instance1.load()
    
    # Проверка: утверждаем, что настройки появились у обоих менеджеров и они одинаковые
    assert instance1.settings is not None
    assert instance2.settings is not None
    assert instance1.settings == instance2.settings