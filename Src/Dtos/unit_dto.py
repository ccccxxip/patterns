class unit_dto:
    """DTO для единицы измерения"""
    id: str = ""
    name: str = ""
    ratio: float = 1.0
    base_unit = None  

    @classmethod
    def from_dict(cls, data: dict) -> "unit_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None
        dto = cls()
        dto.id = str(data.get("id", ""))
        dto.name = str(data.get("name", ""))
        dto.ratio = float(data.get("ratio", 1.0))
        base = data.get("base_unit")
        dto.base_unit = cls.from_dict(base) if isinstance(base, dict) else None
        return dto