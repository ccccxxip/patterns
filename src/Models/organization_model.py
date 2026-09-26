from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.constants import INN_VALID_LENGTHS, BIK_LENGTH, ACCOUNT_LENGTH


class organization_model(base_model):
    """
    Модель данных "Организация"
    Наследуется от base_model
    """

    def __init__(self, name: str, inn: str, bik: str, account: str, ownership_form: str) -> None:
        """
        Инициализирует экземпляр модели организации

        name: Наименование организации (валидируется в base_model)
        inn: ИНН организации (10 или 12 цифр)
        bik: БИК банка организации (9 цифр)
        account: Расчетный счет организации (20 цифр)
        ownership_form: Форма собственности организации (ООО, ИП, АО)
        """
        super().__init__()
        self.name = name
        self.inn = inn
        self.bik = bik
        self.account = account
        self.ownership_form = ownership_form

    @property
    def inn(self) -> str:
        """Возвращает ИНН организации"""
        return self._inn

    @inn.setter
    def inn(self, value: str) -> None:
        """Задаёт ИНН организации (10 или 12 цифр)"""
        if not isinstance(value, str):
            raise arguments_exception("inn", "ИНН должен быть строкой")

        normalized_value = value.strip()

        if not normalized_value.isdigit():
            raise arguments_exception("inn", "ИНН должен содержать только цифры")

        if len(normalized_value) not in INN_VALID_LENGTHS:
            raise arguments_exception("inn", "ИНН должен состоять из 10 (юр.лицо) или 12 (ИП) цифр")

        self._inn = normalized_value

    @property
    def bik(self) -> str:
        """Возвращает БИК банка организации"""
        return self._bik

    @bik.setter
    def bik(self, value: str) -> None:
        """Задаёт БИК банка организации (9 цифр)"""
        if not isinstance(value, str):
            raise arguments_exception("bik", "БИК должен быть строкой")

        normalized_value = value.strip()

        if not normalized_value.isdigit():
            raise arguments_exception("bik", "БИК должен содержать только цифры")

        if len(normalized_value) != BIK_LENGTH:
            raise arguments_exception("bik", f"БИК должен состоять из {BIK_LENGTH} цифр")

        self._bik = normalized_value

    @property
    def account(self) -> str:
        """Возвращает расчетный счет организации"""
        return self._account

    @account.setter
    def account(self, value: str) -> None:
        """Задаёт расчетный счет организации (20 цифр)"""
        if not isinstance(value, str):
            raise arguments_exception("account", "Расчетный счет должен быть строкой")

        normalized_value = value.strip()

        if not normalized_value.isdigit():
            raise arguments_exception("account", "Расчетный счет должен содержать только цифры")

        if len(normalized_value) != ACCOUNT_LENGTH:
            raise arguments_exception("account", f"Расчетный счет должен состоять из {ACCOUNT_LENGTH} цифр")

        self._account = normalized_value

    @property
    def ownership_form(self) -> str:
        """Возвращает форму собственности организации"""
        return self._ownership_form

    @ownership_form.setter
    def ownership_form(self, value: str) -> None:
        """Задаёт форму собственности организации"""
        if not isinstance(value, str):
            raise arguments_exception("ownership_form", "Форма собственности должна быть строкой")

        normalized_value = value.strip()

        if not normalized_value:
            raise arguments_exception("ownership_form", "Форма собственности не может быть пустой")

        self._ownership_form = normalized_value