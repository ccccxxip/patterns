from Src.Dtos.warehouse_dto import warehouse_dto
from Src.Dtos.unit_dto import unit_dto
from Src.Dtos.nomenclature_group_dto import nomenclature_group_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.ingredient_dto import ingredient_dto
from Src.Dtos.recipe_dto import recipe_dto


class storage_dto:
    """Корневой DTO всего хранилища данных"""
    warehouse: list = None
    unit: list = None
    group: list = None
    nomenclature: list = None
    recipe: list = None

    @classmethod
    def from_dict(cls, data: dict) -> "storage_dto":
        """Создание DTO из словаря"""
        if not isinstance(data, dict):
            return None

        def parse_list(key: str, dto_cls):
            items = data.get(key, [])
            if not isinstance(items, list):
                return []
            return [dto_cls.from_dict(item) for item in items if isinstance(item, dict)]

        dto = cls()
        dto.warehouse = parse_list("warehouse", warehouse_dto)
        dto.unit = parse_list("unit", unit_dto)
        dto.group = parse_list("group", nomenclature_group_dto)
        dto.nomenclature = parse_list("nomenclature", nomenclature_dto)
        dto.recipe = parse_list("recipe", recipe_dto)
        return dto