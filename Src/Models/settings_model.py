from Src.Core.base_model import base_model
from Src.Models.organization_model import organization_model
from Src.Core.validator import validator
from Src.Dtos.report_type_dto import report_type_enum


class settings_model(base_model):
    """
    Модель настроек
    Хранит глобальные параметры системы и защищает их от записи некорректных данных
    с помощью инкапсуляции и валидации
    """

    __organization: organization_model = None
    __boss_name: str = ""
    __account_name: str = ""
    __is_first_start: bool = True
    __response_format: report_type_enum = report_type_enum.TXT


    @property
    def organization(self) -> organization_model:
        """Экземпляр модели организации с реквизитами компании"""
        return self.__organization

    @organization.setter
    def organization(self, value: organization_model) -> None:
        validator.validate(value, organization_model, field_name="organization")
        self.__organization = value

    @property
    def boss_name(self) -> str:
        """ФИО директора"""
        return self.__boss_name

    @boss_name.setter
    def boss_name(self, value: str) -> None:
        validator.validate(value, str, 255, field_name="boss_name")
        self.__boss_name = value.strip()

    @property
    def account_name(self) -> str:
        """Наименование банковского счета"""
        return self.__account_name

    @account_name.setter
    def account_name(self, value: str) -> None:
        validator.validate(value, str, 255, field_name="account_name")
        self.__account_name = value.strip()

    @property
    def is_first_start(self) -> bool:
        """Флаг первого запуска """
        return self.__is_first_start

    @is_first_start.setter
    def is_first_start(self, value: bool) -> None:
        validator.validate(value, bool, field_name="is_first_start")
        self.__is_first_start = value

    @property
    def response_format(self) -> report_type_enum:
        """Формат вывода отчётов по умолчанию"""
        return self.__response_format

    @response_format.setter
    def response_format(self, value: report_type_enum) -> None:
        """Задаёт формат вывода отчётов по умолчанию"""
        validator.validate(value, report_type_enum, field_name="response_format")
        self.__response_format = value
