class nomenclature_group_dto:
    """DTO для группы номенклатуры"""

    def __init__(self, id: str = "", name: str = ""):
        self.id = str(id) if id is not None else ""
        self.name = str(name) if name is not None else ""

    @classmethod
    def from_dict(cls, data: dict) -> "nomenclature_group_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None

        return cls(
            id=data.get("id", ""),
            name=data.get("name", "")
        )