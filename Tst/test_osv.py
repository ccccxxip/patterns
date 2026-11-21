from Src.Models.osv_row_model import osv_row_model
from Src.Models.warehouse_model import warehouse_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.unit_model import unit_model
from Src.Logics.osv_service import osv_service
from Src.Dtos.filter_dto import filter_dto
from Src.Core.filter_type import filter_type
from Src.Logics.storage_manager import storage_manager


def test_osv_row_model_properties_and_recalc():
    """
    Сценарий: Проверка свойств и автоматического перерасчета конечного остатка в osv_row_model
    Ожидаемый результат: end_balance = start_balance + turnover_in - turnover_out
    """
    # Подготовка
    row = osv_row_model()
    row.start_balance = 100.0
    row.turnover_in = 45.5
    row.turnover_out = 20.5

    # Действие
    end_balance = row.end_balance

    # Проверка
    assert end_balance == 125.0
    assert osv_row_model.warehouse.__doc__ is not None
    assert osv_row_model.nomenclature.__doc__ is not None


def test_osv_service_build_without_filter():
    """
    Сценарий: Формирование ОСВ без фильтра
    Ожидаемый результат: Возвращается полный список строк по всем номенклатурам
    """
    # Подготовка
    sm = storage_manager()
    noms = sm.get_entities_by_type("nomenclature")
    service = osv_service(sm)

    # Действие
    rows = service.build()

    # Проверка
    assert len(rows) == len(noms)
    for r in rows:
        assert isinstance(r, osv_row_model)
        assert r.nomenclature is not None
        assert r.end_balance == round(r.start_balance + r.turnover_in - r.turnover_out, 4)


def test_osv_service_build_filtered_by_name():
    """
    Сценарий: Формирование ОСВ с фильтрацией по наименованию номенклатуры через Прототип
    Ожидаемый результат: Возвращаются только строки ведомости с указанной номенклатурой
    """
    # Подготовка
    service = osv_service()
    f = filter_dto()
    f.name = "Куриное филе"
    f.filter_type = filter_type.EQUALS

    # Действие
    rows = service.build(f)

    # Проверка
    assert len(rows) == 1
    assert rows[0].nomenclature.name == "Куриное филе"


def test_osv_service_build_filtered_by_nested_group():
    """
    Сценарий: Формирование ОСВ с фильтрацией по вложенной группе номенклатуры через Прототип
    Ожидаемый результат: Возвращаются строки ОСВ только для позиций из группы 'Сырье'
    """
    # Подготовка
    service = osv_service()
    f = filter_dto()
    f.name = "Сырье"
    f.filter_type = filter_type.EQUALS

    # Действие
    rows = service.build(f)

    # Проверка
    assert len(rows) > 0
    for r in rows:
        assert r.nomenclature.group.name == "Сырье"