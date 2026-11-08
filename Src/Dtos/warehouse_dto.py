class warehouse_dto:
    """DTO для описания склада"""

    def __init__(self, id: str = "", name: str = "", address: str = ""):
        self.id = str(id) if id is not None else ""
        self.name = str(name) if name is not None else ""
        self.address = str(address) if address is not None else ""

    @classmethod
    def from_dict(cls, data: dict) -> "warehouse_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            address=data.get("address", "")
        )