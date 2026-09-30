from Src.Models.nomenclature_group_model import nomenclature_group_model


def test_create_nomenclature_group_with_valid_name_returns_object_with_name():
    """
    Сценарий: создание группы номенклатуры с валидным названием
    Ожидаемый результат: объект создается, название сохраняется, id не пустой
    """
    group = nomenclature_group_model("Мясная продукция")

    assert group.name == "Мясная продукция"
    assert group.id != ""