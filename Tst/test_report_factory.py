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
    Сценарий: создание отчёта по типу CSV через метод create фабрики
    Ожидаемый результат: фабрика возвращает экземпляр класса csv_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.CSV)

    # Проверка
    assert report is not None
    assert isinstance(report, csv_report)


def test_factory_create_markdown():
    """
    Сценарий: создание отчёта по типу MARKDOWN через метод create фабрики
    Ожидаемый результат: фабрика возвращает экземпляр класса markdown_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.MARKDOWN)

    # Проверка
    assert report is not None
    assert isinstance(report, markdown_report)


def test_factory_create_xml():
    """
    Сценарий: создание отчёта по типу XML через метод create фабрики
    Ожидаемый результат: фабрика возвращает экземпляр класса xml_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.XML)

    # Проверка
    assert report is not None
    assert isinstance(report, xml_report)


def test_factory_create_html():
    """
    Сценарий: создание отчёта по типу HTML через метод create фабрики
    Ожидаемый результат: фабрика возвращает экземпляр класса html_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.HTML)

    # Проверка
    assert report is not None
    assert isinstance(report, html_report)


def test_factory_create_txt():
    """
    Сценарий: создание отчёта по типу TXT через метод create фабрики
    Ожидаемый результат: фабрика возвращает экземпляр класса text_report
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create(report_type_enum.TXT)

    # Проверка
    assert report is not None
    assert isinstance(report, text_report)


def test_factory_create_default():
    """
    Сценарий: создание отчёта по умолчанию методом create_default без указания типа
    Ожидаемый результат: фабрика возвращает отчёт того формата, который задан в настройках
    """
    # Подготовка
    factory = report_factory()

    # Действие
    report = factory.create_default()

    # Проверка
    assert report is not None


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
