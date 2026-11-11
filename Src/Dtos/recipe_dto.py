from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.ingredient_dto import ingredient_dto


class recipe_dto:
    """DTO для технологической карты (рецепта)"""
    id: str = ""
    name: str = ""
    portions: int = 1
    preparation_method: str = ""
    total_gross_weight: float = 0.0
    total_net_weight: float = 0.0
    owner = None
    ingredients: list = None

    @classmethod
    def from_dict(cls, data: dict) -> "recipe_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None
        dto = cls()
        dto.id = str(data.get("id", ""))
        dto.name = str(data.get("name", ""))
        dto.portions = int(data.get("portions", 1))
        dto.preparation_method = str(data.get("preparation_method", ""))
        dto.total_gross_weight = float(data.get("total_gross_weight", 0.0))
        dto.total_net_weight = float(data.get("total_net_weight", 0.0))
        owner = data.get("owner")
        dto.owner = nomenclature_dto.from_dict(owner) if isinstance(owner, dict) else None
        raw = data.get("ingredients", [])
        dto.ingredients = [
            ingredient_dto.from_dict(item)
            for item in raw
            if isinstance(item, dict)
        ] if isinstance(raw, list) else []
        return dto