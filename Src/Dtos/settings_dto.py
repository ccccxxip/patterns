from Src.Dtos.organization_dto import organization_dto
from Src.Core.common import common

class settings_dto:
    """DTO для описания глобальных настроек"""

    def __init__(self):
        self._organization = None
        self._boss_name: str = ""
        self._account_name: str = ""
        self._is_first_start: bool = True
        self._response_format: str = "TXT"

    @property
    def organization(self):
        """Реквизиты организации"""
        return self._organization

    @organization.setter
    def organization(self, value):
        self._organization = value

    @property
    def boss_name(self) -> str:
        """ФИО руководителя"""
        return self._boss_name

    @boss_name.setter
    def boss_name(self, value: str):
        self._boss_name = str(value) if value is not None else ""

    @property
    def account_name(self) -> str:
        """Наименование расчетного счета"""
        return self._account_name

    @account_name.setter
    def account_name(self, value: str):
        self._account_name = str(value) if value is not None else ""

    @property
    def is_first_start(self) -> bool:
        """Флаг первого запуска системы"""
        return self._is_first_start

    @is_first_start.setter
    def is_first_start(self, value: bool):
        self._is_first_start = bool(value)

    @property
    def response_format(self) -> str:
        """Формат вывода отчетов по умолчанию"""
        return self._response_format

    @response_format.setter
    def response_format(self, value: str):
        self._response_format = str(value) if value is not None else "TXT"

    @classmethod
    def from_dict(cls, data: dict) -> "settings_dto":
        """
        Создание DTO из словаря с использованием рефлексии
        Если организация не указана -> None
        """
        if not isinstance(data, dict):
            return None

        dto = cls()
        fields = common.get_fields(dto)

        for field in fields:
            if field not in data:
                continue

            value = data[field]
            if field == "organization":
                dto.organization = organization_dto.from_dict(value) if isinstance(value, dict) else None
            else:
                setattr(dto, field, value)

        return dto