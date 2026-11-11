class warehouse_dto:
    """DTO для описания склада"""
    id: str = ""
    name: str = ""
    address: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "warehouse_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None
        dto = cls()
        dto.id = str(data.get("id", ""))
        dto.name = str(data.get("name", ""))
        dto.address = str(data.get("address", ""))
        return dto