import pytest
from Src.Logics.report_factory import report_factory
from Src.Logics.text_report import text_report
from Src.Logics.csv_report import csv_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.xml_report import xml_report
from Src.Logics.html_report import html_report
from Src.Dtos.report_type_dto import report_type_enum
from Src.Core.exception import arguments_exception


def test_factory_create_csv():
    """
    Сценарий: подбор класса отчёта по типу CSV через метод create фабрики
    Ожидаемый результат: фабрика возвращает класс csv_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report_cls = factory.create(report_type_enum.CSV)

    # Проверка
    assert report_cls is not None
    assert report_cls is csv_report


def test_factory_create_markdown():
    """
    Сценарий: подбор класса отчёта по типу MARKDOWN через метод create фабрики
    Ожидаемый результат: фабрика возвращает класс markdown_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report_cls = factory.create(report_type_enum.MARKDOWN)

    # Проверка
    assert report_cls is not None
    assert report_cls is markdown_report


def test_factory_create_xml():
    """
    Сценарий: подбор класса отчёта по типу XML через метод create фабрики
    Ожидаемый результат: фабрика возвращает класс xml_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report_cls = factory.create(report_type_enum.XML)

    # Проверка
    assert report_cls is not None
    assert report_cls is xml_report


def test_factory_create_html():
    """
    Сценарий: подбор класса отчёта по типу HTML через метод create фабрики
    Ожидаемый результат: фабрика возвращает класс html_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report_cls = factory.create(report_type_enum.HTML)

    # Проверка
    assert report_cls is not None
    assert report_cls is html_report


def test_factory_create_txt():
    """
    Сценарий: подбор класса отчёта по типу TXT через метод create фабрики
    Ожидаемый результат: фабрика возвращает класс text_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report_cls = factory.create(report_type_enum.TXT)

    # Проверка
    assert report_cls is not None
    assert report_cls is text_report


def test_factory_create_default():
    """
    Сценарий: подбор класса отчёта по умолчанию методом create_default без указания типа
    Ожидаемый результат: фабрика возвращает класс отчёта того формата, который задан в настройках
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report_cls = factory.create_default()

    # Проверка
    assert report_cls is not None


def test_factory_create_invalid_raises():
    """
    Сценарий: передача неподдерживаемого типа отчёта в метод create
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    # Подготовка
    factory = report_factory()
    is_exception = False

    # Действие
    try:
        factory.create("INVALID_TYPE")
    except arguments_exception:
        is_exception = True

    # Проверка
    assert is_exception is True


def test_factory_create_returns_callable():
    """
    Сценарий: проверка что подобранный фабрикой класс можно инстанциировать
    Ожидаемый результат: вызов класса с () создаёт экземпляр нужного отчёта
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report_cls = factory.create(report_type_enum.CSV)
    report_obj = report_cls()

    # Проверка
    assert isinstance(report_obj, csv_report)
