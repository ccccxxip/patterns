from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.unit_dto import unit_dto


class ingredient_dto:
    """DTO для строки ингредиента рецепта"""

    def __init__(self, id: str = "", name: str = "", gross_weight: float = 0.0,
                 net_weight: float = 0.0, nomenclature: nomenclature_dto = None,
                 unit: unit_dto = None, recipe: object = None):
        self.id = str(id) if id is not None else ""
        self.name = str(name) if name is not None else ""
        self.gross_weight = float(gross_weight) if gross_weight is not None else 0.0
        self.net_weight = float(net_weight) if net_weight is not None else 0.0
        self.nomenclature = nomenclature
        self.unit = unit
        self.recipe = recipe

    @classmethod
    def from_dict(cls, data: dict) -> "ingredient_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None

        # проверка ключа recipe
        recipe_obj = None
        if "recipe" in data and isinstance(data["recipe"], dict):

            from Src.Dtos.recipe_dto import recipe_dto
            recipe_obj = recipe_dto.from_dict(data["recipe"])

        # проверка ключа nomenclature
        nom_obj = None
        if "nomenclature" in data and isinstance(data["nomenclature"], dict):
            nom_obj = nomenclature_dto.from_dict(data["nomenclature"])

        # проверка ключа unit
        unit_obj = None
        if "unit" in data and isinstance(data["unit"], dict):
            unit_obj = unit_dto.from_dict(data["unit"])

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            gross_weight=data.get("gross_weight", 0.0),
            net_weight=data.get("net_weight", 0.0),
            nomenclature=nom_obj,
            unit=unit_obj,
            recipe=recipe_obj
        )