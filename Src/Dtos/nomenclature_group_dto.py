class nomenclature_group_dto:
    """DTO для группы номенклатуры"""
    id: str = ""
    name: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "nomenclature_group_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None
        dto = cls()
        dto.id = str(data.get("id", ""))
        dto.name = str(data.get("name", ""))
        return dto