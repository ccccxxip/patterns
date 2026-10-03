import pytest
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Models.unit_model import unit_model


def test_storage_manager_singleton():
    """
    Сценарий: многократное создание экземпляров менеджера хранилища
    Ожидаемый результат: Singleton гарантирует, что возвращается один и тот же объект,
    и они делят общее хранилище данных (data)
    """
    # Подготовка и Действие: создаем два менеджера
    mgr1 = storage_manager()
    mgr2 = storage_manager()
    
    # Проверка: утверждаем, что это один и тот же участок памяти
    assert mgr1 is mgr2
    assert mgr1.data is mgr2.data


def test_storage_manager_add_uniqueness():
    """
    Сценарий: добавление одного и того же объекта в хранилище несколько раз
    Ожидаемый результат: срабатывает защита от дубликатов, объект сохраняется только один раз
    """
    # Подготовка: получаем менеджер, очищаем список единиц и создаем тестовый объект
    mgr = storage_manager()
    mgr.units.clear()  # Очищаем перед тестом, чтобы старые данные не мешали
    test_unit = unit_model("Литр", 1000)
    
    # Действие: пытаемся добавить один и тот же объект дважды
    mgr.add("unit", test_unit)
    mgr.add("unit", test_unit)
    
    # Проверка: утверждаем, что в списке остался ровно 1 элемент
    assert len(mgr.units) == 1


def test_storage_manager_first_start_generates_data():
    """
    Сценарий: запуск хранилища при активном флаге первого старта (is_first_start = True)
    Ожидаемый результат: хранилище автоматически генерирует стартовый набор данных 
    и отключает флаг первого старта
    """
    # Подготовка: 
    # Настраиваем settings_manager как будто программа запущена впервые
    set_mgr = settings_manager()
    set_mgr.load()  
    set_mgr.settings.is_first_start = True  # Принудительно включаем первый старт
    
    # Получаем storage_manager и очищаем все ящики 
    st_mgr = storage_manager()
    st_mgr.units.clear()
    st_mgr.groups.clear()
    st_mgr.warehouses.clear()
    st_mgr.nomenclatures.clear()
    
    # Действие: запускаем загрузку хранилища
    st_mgr.load()
    
    # Проверка: 
    # Флаг первого старта должен быть отключен, чтобы генерация не повторялась
    assert set_mgr.settings.is_first_start is False
    
    # 2. Проверяем, что все стартовые данные правильные
    assert len(st_mgr.units) == 5           # Грамм, Кг, Миллилитр, Литр, Штука  
    assert len(st_mgr.groups) == 1          # Ингредиенты
    assert len(st_mgr.warehouses) == 1      # Основной склад
    assert len(st_mgr.nomenclatures) == 2   # Мука и Сахар