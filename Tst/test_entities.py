from Src.Core.base_model import base_model

# тестовая сущность 
class test_entity(base_model):
    pass

def test_base_model_get_id_not_null():
    entity = test_entity()
    assert entity.id != ""

def test_base_model_unique_id_for_different_instances():
    entity1 = test_entity()
    entity2 = test_entity()
    assert entity1.id != entity2.id

def test_entities_with_same_id_are_equal():
    # подготовка
    entity1 = test_entity()
    entity2 = test_entity()

    # действие — используем сеттер
    entity1.id = "12345"
    entity2.id = "12345"

    # проверка
    assert entity1 == entity2

def test_name_setter_empty_string_raises_exception():
    entity = test_entity()
    is_exception = False

    try:
        entity.name = ""
    except Exception: 
        is_exception = True

    assert is_exception is True