from Src.Dtos.nomenclature_group_dto import nomenclature_group_dto
from Src.Dtos.unit_dto import unit_dto


class nomenclature_dto:
    """DTO для номенклатуры"""

    def __init__(self, id: str = "", name: str = "", full_name: str = "",
                 group: nomenclature_group_dto = None, unit: unit_dto = None,
                 nom_type: str = ""):
        self.id = str(id) if id is not None else ""
        self.name = str(name) if name is not None else ""
        self.full_name = str(full_name) if full_name is not None else ""
        self.group = group
        self.unit = unit
        self.type = str(nom_type) if nom_type is not None else ""

    @classmethod
    def from_dict(cls, data: dict) -> "nomenclature_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None

        # проверка группы
        group_obj = None
        if "group" in data and isinstance(data["group"], dict):
            group_obj = nomenclature_group_dto.from_dict(data["group"])

        # проверка единицы измерения
        unit_obj = None
        if "unit" in data and isinstance(data["unit"], dict):
            unit_obj = unit_dto.from_dict(data["unit"])

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            full_name=data.get("full_name", ""),
            group=group_obj,
            unit=unit_obj,
            nom_type=data.get("type", "")
        )