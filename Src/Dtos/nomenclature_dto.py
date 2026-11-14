from Src.Dtos.nomenclature_group_dto import nomenclature_group_dto
from Src.Dtos.unit_dto import unit_dto


class nomenclature_dto:
    """DTO для номенклатуры"""
    id: str = ""
    name: str = ""
    full_name: str = ""
    type: str = ""
    group = None
    unit = None

    @classmethod
    def from_dict(cls, data: dict) -> "nomenclature_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None
        dto = cls()
        dto.id = str(data.get("id", ""))
        dto.name = str(data.get("name", ""))
        dto.full_name = str(data.get("full_name", ""))
        dto.type = str(data.get("type", ""))
        group = data.get("group")
        dto.group = nomenclature_group_dto.from_dict(group) if isinstance(group, dict) else None
        unit = data.get("unit")
        dto.unit = unit_dto.from_dict(unit) if isinstance(unit, dict) else None
        return dto