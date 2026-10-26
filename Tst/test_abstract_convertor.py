import inspect
import pytest
from Src.Core.abstract_convertor import abstract_convertor


def test_abstract_convertor_is_abstract():
    """
    Сценарий: Проверка абстрактности класса abstract_convertor
    Ожидаемый результат: inspect.isabstract возвращает True, создание экземпляра вызывает TypeError
    """
    # Подготовка и Проверка: класс является абстрактным
    assert inspect.isabstract(abstract_convertor) is True

    # Действие и Проверка: попытка создания вызывает TypeError
    with pytest.raises(TypeError):
        globals()["abstract_convertor"]()


def test_abstract_convertor_subclass_without_implementation_is_abstract():
    """
    Сценарий: Создание класса-наследника без реализации абстрактного метода Convert
    Ожидаемый результат: Класс-наследник также остается абстрактным
    """
    # Подготовка
    class incomplete_convertor(abstract_convertor):
        pass

    # Действие и Проверка
    assert inspect.isabstract(incomplete_convertor) is True


def test_abstract_convertor_subclass_with_implementation_success():
    """
    Сценарий: Создание наследника с корректной реализацией метода Convert
    Ожидаемый результат: Экземпляр успешно создается, метод Convert возвращает словарь
    """
    # Подготовка
    class dummy_convertor(abstract_convertor):
        def Convert(self, item: object, field_name: str = None) -> dict:
            return {"dummy": item}

    # Действие: класс перестает быть абстрактным
    assert inspect.isabstract(dummy_convertor) is False
    conv = dummy_convertor()

    # Проверка
    assert conv.Convert("test") == {"dummy": "test"}
