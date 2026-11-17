from Src.Core.common import common


class organization_dto:
    """DTO для описания реквизитов организации"""

    def __init__(self):
        self._name: str = ""
        self._inn: str = ""
        self._bik: str = ""
        self._account: str = ""
        self._ownership_form: str = ""

    @property
    def name(self) -> str:
        """Наименование организации"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = str(value).strip() if value is not None else ""

    @property
    def inn(self) -> str:
        """ИНН организации"""
        return self._inn

    @inn.setter
    def inn(self, value: str):
        self._inn = str(value).strip() if value is not None else ""

    @property
    def bik(self) -> str:
        """БИК банка организации"""
        return self._bik

    @bik.setter
    def bik(self, value: str):
        self._bik = str(value).strip() if value is not None else ""

    @property
    def account(self) -> str:
        """Расчетный счет организации"""
        return self._account

    @account.setter
    def account(self, value: str):
        self._account = str(value).strip() if value is not None else ""

    @property
    def ownership_form(self) -> str:
        """Форма собственности организации"""
        return self._ownership_form

    @ownership_form.setter
    def ownership_form(self, value: str):
        self._ownership_form = str(value).strip() if value is not None else ""

    @classmethod
    def from_dict(cls, data: dict) -> "organization_dto":
        """
        Создание DTO из словаря с использованием рефлексии
        """
        if not isinstance(data, dict):
            return None

        dto = cls()
        fields = common.get_fields(dto)

        # Проверка наличия всех свойств DTO во входном словаре через рефлексию
        if not set(fields).issubset(data.keys()):
            return None

        # Заполнение значений свойств через рефлексию
        for field in fields:
            setattr(dto, field, data[field])

        return dto