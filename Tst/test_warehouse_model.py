import pytest
from Src.Models.warehouse_model import warehouse_model
from Src.Core.exception import arguments_exception


def test_create_warehouse_with_valid_data_returns_object():
    """
    Сценарий: создание объекта склада с обычным непустым названием и адресом
    Ожидаемый результат: объект создается, наименование и адрес сохраняются, id сгенерирован
    """
    warehouse = warehouse_model("Склад производственного цеха", "ул. Промышленная, д. 10")

    assert warehouse.name == "Склад производственного цеха"
    assert warehouse.address == "ул. Промышленная, д. 10"
    assert warehouse.id != ""


def test_create_warehouse_with_empty_address_raises_exception():
    """
    Сценарий: создание склада с пустым адресом
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    with pytest.raises(arguments_exception):
        warehouse_model("Склад", "   ")


def test_create_warehouse_with_invalid_address_type_raises_exception():
    """
    Сценарий: создание склада с адресом неверного типа (например, числом)
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    with pytest.raises(arguments_exception):
        warehouse_model("Склад", 12345)