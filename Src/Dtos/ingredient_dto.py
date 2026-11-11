from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.unit_dto import unit_dto


class ingredient_dto:
    """DTO для строки ингредиента рецепта"""
    id: str = ""
    name: str = ""
    gross_weight: float = 0.0
    net_weight: float = 0.0
    nomenclature = None 
    unit = None 
    recipe = None

    @classmethod
    def from_dict(cls, data: dict) -> "ingredient_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None
        dto = cls()
        dto.id = str(data.get("id", ""))
        dto.name = str(data.get("name", ""))
        dto.gross_weight = float(data.get("gross_weight", 0.0))
        dto.net_weight = float(data.get("net_weight", 0.0))
        nom = data.get("nomenclature")
        dto.nomenclature = nomenclature_dto.from_dict(nom) if isinstance(nom, dict) else None
        unit = data.get("unit")
        dto.unit = unit_dto.from_dict(unit) if isinstance(unit, dict) else None
        recipe = data.get("recipe")
        if isinstance(recipe, dict):
            from Src.Dtos.recipe_dto import recipe_dto
            dto.recipe = recipe_dto.from_dict(recipe)
        return dto