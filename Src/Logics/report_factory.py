from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_type_dto import report_type_enum
from Src.Core.exception import arguments_exception
from Src.Logics.text_report import text_report
from Src.Logics.markdown_report import markdown_report
from Src.Logics.csv_report import csv_report
from Src.Logics.xml_report import xml_report
from Src.Logics.html_report import html_report


class report_factory:
    """
    Фабрика отчётов
    Инкапсулирует маппинг типов и настройки
    Создаёт нужный отчёт по указанному типу или по формату из настроек
    """

    __mapping: dict = {
        report_type_enum.TXT:      text_report,
        report_type_enum.CSV:      csv_report,
        report_type_enum.MARKDOWN: markdown_report,
        report_type_enum.XML:      xml_report,
        report_type_enum.HTML:     html_report,
    }

    def __init__(self):
        """Инициализирует фабрику и загружает настройки"""
        from Src.Logics.settings_manager import settings_manager
        self.__settings_manager = settings_manager()
        if not self.__settings_manager.is_loaded:
            self.__settings_manager.load()

    def create(self, report_type: report_type_enum) -> abstract_report:
        """Создаёт отчёт указанного типа"""
        if report_type not in self.__mapping:
            raise arguments_exception(
                "report_type",
                f"Указанный тип отчёта '{report_type}' не поддерживается"
            )
        return self.__mapping[report_type]()

    def create_default(self) -> abstract_report:
        """Создаёт отчёт в формате по умолчанию из настроек (response_format)"""
        default_format = self.__settings_manager.settings.response_format
        return self.create(default_format)
