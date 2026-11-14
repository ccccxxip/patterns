from Src.Dtos.organization_dto import organization_dto


class settings_dto:
    """DTO для описания глобальных настроек"""
    organization = None
    boss_name: str = ""
    account_name: str = ""
    is_first_start: bool = True
    response_format: str = "TXT"

    @classmethod
    def from_dict(cls, data: dict) -> "settings_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None

        dto = cls()
        org_data = data.get("organization")
        dto.organization = organization_dto.from_dict(org_data) if isinstance(org_data, dict) else None

        dto.boss_name = str(data.get("boss_name", ""))
        dto.account_name = str(data.get("account_name", ""))
        if "is_first_start" in data:
            dto.is_first_start = bool(data.get("is_first_start"))

        dto.response_format = str(data.get("response_format", "TXT"))
        return dto