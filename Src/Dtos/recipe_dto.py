from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.ingredient_dto import ingredient_dto


class recipe_dto:
    """DTO для технологической карты (рецепта)"""

    def __init__(self, id: str = "", name: str = "", portions: int = 1,
                 preparation_method: str = "", total_gross_weight: float = 0.0,
                 total_net_weight: float = 0.0, owner: nomenclature_dto = None,
                 ingredients: list = None):
        self.id = str(id) if id is not None else ""
        self.name = str(name) if name is not None else ""
        self.portions = int(portions) if portions is not None else 1
        self.preparation_method = str(preparation_method) if preparation_method is not None else ""
        self.total_gross_weight = float(total_gross_weight) if total_gross_weight is not None else 0.0
        self.total_net_weight = float(total_net_weight) if total_net_weight is not None else 0.0
        self.owner = owner
        self.ingredients = ingredients if ingredients is not None else []

    @classmethod
    def from_dict(cls, data: dict) -> "recipe_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None

        # проверка владельца рецепта
        owner_obj = None
        if "owner" in data and isinstance(data["owner"], dict):
            owner_obj = nomenclature_dto.from_dict(data["owner"])

        # проверка списка ингредиентов
        raw_ingredients = []
        if "ingredients" in data and isinstance(data["ingredients"], list):
            raw_ingredients = [
                ingredient_dto.from_dict(item)
                for item in data["ingredients"]
                if isinstance(item, dict)
            ]

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            portions=data.get("portions", 1),
            preparation_method=data.get("preparation_method", ""),
            total_gross_weight=data.get("total_gross_weight", 0.0),
            total_net_weight=data.get("total_net_weight", 0.0),
            owner=owner_obj,
            ingredients=raw_ingredients
        )