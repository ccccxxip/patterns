from Src.Models.warehouse_model import warehouse_model


def test_create_warehouse_with_valid_name_returns_object_with_name():
    """
    Сценарий: создание объекта склада с обычным непустым названием
    Ожидаемый результат: объект создается, наименование сохраняется, id автоматически сгенерирован
    """
    warehouse = warehouse_model("Склад производственного цеха")

    assert warehouse.name == "Склад производственного цеха"
    assert warehouse.id != ""