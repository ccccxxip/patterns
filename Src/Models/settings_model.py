from Src.Core.base_model import base_model
from Src.Models.organization_model import organization_model
from Src.Core.validator import validator


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