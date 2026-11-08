class unit_dto:
    """DTO для единицы измерения"""

    def __init__(self, id: str = "", name: str = "", ratio: float = 1.0, base_unit: "unit_dto" = None):
        self.id = str(id) if id is not None else ""
        self.name = str(name) if name is not None else ""
        self.ratio = float(ratio) if ratio is not None else 1.0
        self.base_unit = base_unit

    @classmethod
    def from_dict(cls, data: dict) -> "unit_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None

        # проверка наличия и типа base_unit
        base_unit_obj = None
        if "base_unit" in data and isinstance(data["base_unit"], dict):
            base_unit_obj = cls.from_dict(data["base_unit"])

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            ratio=data.get("ratio", 1.0),
            base_unit=base_unit_obj
        )