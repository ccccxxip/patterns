from Src.Dtos.warehouse_dto import warehouse_dto
from Src.Dtos.unit_dto import unit_dto
from Src.Dtos.nomenclature_group_dto import nomenclature_group_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.ingredient_dto import ingredient_dto
from Src.Dtos.recipe_dto import recipe_dto


class storage_dto:
    """Корневой DTO всего хранилища данных"""

    def __init__(self, warehouse: list = None, unit: list = None,
                 group: list = None, nomenclature: list = None,
                 recipe: list = None):
        self.warehouse = warehouse if warehouse is not None else []
        self.unit = unit if unit is not None else []
        self.group = group if group is not None else []
        self.nomenclature = nomenclature if nomenclature is not None else []
        self.recipe = recipe if recipe is not None else []

    @classmethod
    def from_dict(cls, data: dict) -> "storage_dto":
        """Фабричный метод десериализации хранилища из словаря"""
        if not isinstance(data, dict):
            return None

        def parse_list(key: str, dto_cls):
            if key in data and isinstance(data[key], list):
                return [dto_cls.from_dict(item) for item in data[key] if isinstance(item, dict)]
            return []

        return cls(
            warehouse=parse_list("warehouse", warehouse_dto),
            unit=parse_list("unit", unit_dto),
            group=parse_list("group", nomenclature_group_dto),
            nomenclature=parse_list("nomenclature", nomenclature_dto),
            recipe=parse_list("recipe", recipe_dto)
        )