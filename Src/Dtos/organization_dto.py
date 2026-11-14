class organization_dto:
    """DTO для описания реквизитов организации"""
    name: str = ""
    inn: str = ""
    bik: str = ""
    account: str = ""
    ownership_form: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "organization_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None

        # Проверка наличия обязательных реквизитов
        required = {"name", "inn", "bik", "account", "ownership_form"}
        if not required.issubset(data.keys()):
            return None

        dto = cls()
        dto.name = str(data.get("name", ""))
        dto.inn = str(data.get("inn", ""))
        dto.bik = str(data.get("bik", ""))
        dto.account = str(data.get("account", ""))
        dto.ownership_form = str(data.get("ownership_form", ""))
        return dto