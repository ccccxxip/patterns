from Src.Core.base_model import base_model
from Src.Models.organization_model import organization_model
from Src.Core.exception import arguments_exception


class settings_model(base_model):

    _organization: organization_model = None
    _boss_name: str = ""
    _account_name: str = ""
    _is_first_start: bool = True

    @property
    def organization(self) -> organization_model:
        return self._organization

    @organization.setter
    def organization(self, value: organization_model) -> None:
        if value is not None and not isinstance(value, organization_model):
            raise arguments_exception("organization", "Некорректная организация")
        self._organization = value

    @property
    def boss_name(self) -> str:
        return self._boss_name

    @boss_name.setter
    def boss_name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise arguments_exception("boss_name", "Некорректное имя руководителя")
        self._boss_name = value.strip()

    @property
    def account_name(self) -> str:
        return self._account_name

    @account_name.setter
    def account_name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise arguments_exception("account_name", "Некорректный счет")
        self._account_name = value.strip()

    @property
    def is_first_start(self) -> bool:
        return self._is_first_start

    @is_first_start.setter
    def is_first_start(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise arguments_exception("is_first_start", "Значение должно быть bool")
        self._is_first_start = value

    def load_from_dict(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise arguments_exception("data", "Данные должны быть словарем")

        if "boss_name" in data and isinstance(data["boss_name"], str):
            self.boss_name = data["boss_name"]

        if "account_name" in data and isinstance(data["account_name"], str):
            self.account_name = data["account_name"]

        if "is_first_start" in data and isinstance(data["is_first_start"], bool):
            self.is_first_start = data["is_first_start"]