import inspect
import pytest
from Src.Core.abstract_convert_factory import abstract_convert_factory
from Src.Logics.convert_factory import convert_factory


def test_abstract_convert_factory_is_abstract():
    """
    Сценарий: Проверка абстрактности класса abstract_convert_factory
    Ожидаемый результат: inspect.isabstract возвращает True, создание экземпляра вызывает TypeError
    """
    # Подготовка и Проверка: класс является абстрактным
    assert inspect.isabstract(abstract_convert_factory) is True

    # Действие и Проверка: попытка создания экземпляра вызывает TypeError
    with pytest.raises(TypeError):
        globals()["abstract_convert_factory"]()



def test_abstract_convert_factory_subclass_without_implementation_is_abstract():
    """
    Сценарий: Создание класса-наследника без реализации абстрактных методов
    Ожидаемый результат: Класс-наследник остается абстрактным
    """
    # Подготовка
    class incomplete_factory(abstract_convert_factory):
        pass

    # Действие и Проверка
    assert inspect.isabstract(incomplete_factory) is True


def test_convert_factory_implements_abstract_convert_factory():
    """
    Сценарий: Проверка реализации фабрики convert_factory от abstract_convert_factory
    Ожидаемый результат: convert_factory наследует abstract_convert_factory, а конвертеры связаны с фабрикой
    """
    # Подготовка
    factory = convert_factory()

    # Действие и Проверка: фабрика наследует абстрактный класс
    assert isinstance(factory, abstract_convert_factory)
    assert issubclass(convert_factory, abstract_convert_factory)

    # Проверка: конвертеры содержат ссылку на создавшую их фабрику
    assert factory.create("basic").factory is factory
    assert factory.create("datetime").factory is factory
    assert factory.create("reference").factory is factory
