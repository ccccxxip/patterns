"""
Слой DTO
Инкапсулирует структуры данных, поступающие из внешних источников (JSON/API),
защищая доменную модель от изменений во внешней схеме данных
"""

class warehouse_dto:
    """DTO для склада"""
    def __init__(self, id: str = "", name: str = "", address: str = ""):
        self.id = id
        self.name = name
        self.address = address

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


class unit_dto:
    """DTO для единицы измерения"""
    def __init__(self, id: str = "", name: str = "", ratio: float = 1.0, base_unit=None):
        self.id = id
        self.name = name
        self.ratio = float(ratio) if ratio is not None else 1.0
        self.base_unit = base_unit

    @classmethod
    def from_dict(cls, data: dict) -> "unit_dto":
        """Фабричный метод создания DTO из словаря (рекурсивный для base_unit)"""
        if not isinstance(data, dict):
            return None
        base_unit_data = data.get("base_unit")
        base_unit_dto = cls.from_dict(base_unit_data) if base_unit_data else None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            ratio=data.get("ratio", 1.0),
            base_unit=base_unit_dto
        )


class nomenclature_group_dto:
    """DTO для группы номенклатуры"""
    def __init__(self, id: str = "", name: str = ""):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, data: dict) -> "nomenclature_group_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", "")
        )


class nomenclature_dto:
    """DTO для номенклатуры"""
    def __init__(self, id: str = "", name: str = "", full_name: str = "",
                 group: nomenclature_group_dto = None, unit: unit_dto = None, nom_type: str = ""):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.group = group
        self.unit = unit
        self.type = nom_type

    @classmethod
    def from_dict(cls, data: dict) -> "nomenclature_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            full_name=data.get("full_name", ""),
            group=nomenclature_group_dto.from_dict(data.get("group")),
            unit=unit_dto.from_dict(data.get("unit")),
            nom_type=data.get("type", "")
        )


class ingredient_dto:
    """DTO для строки технологической карты (ингредиента)"""
    def __init__(self, id: str = "", name: str = "", gross_weight: float = 0.0,
                 net_weight: float = 0.0, nomenclature: nomenclature_dto = None,
                 unit: unit_dto = None, recipe=None):
        self.id = id
        self.name = name
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
        recipe_data = data.get("recipe")
        recipe_obj = recipe_dto.from_dict(recipe_data) if recipe_data else None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            gross_weight=data.get("gross_weight", 0.0),
            net_weight=data.get("net_weight", 0.0),
            nomenclature=nomenclature_dto.from_dict(data.get("nomenclature")),
            unit=unit_dto.from_dict(data.get("unit")),
            recipe=recipe_obj
        )


class recipe_dto:
    """DTO для технологической карты (рецепта)"""
    def __init__(self, id: str = "", name: str = "", portions: int = 1,
                 preparation_method: str = "", total_gross_weight: float = 0.0,
                 total_net_weight: float = 0.0, owner: nomenclature_dto = None,
                 ingredients: list = None):
        self.id = id
        self.name = name
        self.portions = int(portions) if portions is not None else 1
        self.preparation_method = preparation_method
        self.total_gross_weight = float(total_gross_weight) if total_gross_weight is not None else 0.0
        self.total_net_weight = float(total_net_weight) if total_net_weight is not None else 0.0
        self.owner = owner
        self.ingredients = ingredients if ingredients is not None else []

    @classmethod
    def from_dict(cls, data: dict) -> "recipe_dto":
        """Фабричный метод создания DTO из словаря"""
        if not isinstance(data, dict):
            return None
        raw_ingredients = data.get("ingredients", [])
        ingredients_list = [ingredient_dto.from_dict(item) for item in raw_ingredients if isinstance(item, dict)]
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            portions=data.get("portions", 1),
            preparation_method=data.get("preparation_method", ""),
            total_gross_weight=data.get("total_gross_weight", 0.0),
            total_net_weight=data.get("total_net_weight", 0.0),
            owner=nomenclature_dto.from_dict(data.get("owner")),
            ingredients=ingredients_list
        )


class storage_dto:
    """Корневой DTO для всего хранилища"""
    def __init__(self, warehouse: list = None, unit: list = None,
                 group: list = None, nomenclature: list = None, recipe: list = None):
        self.warehouse = warehouse if warehouse is not None else []
        self.unit = unit if unit is not None else []
        self.group = group if group is not None else []
        self.nomenclature = nomenclature if nomenclature is not None else []
        self.recipe = recipe if recipe is not None else []

    @classmethod
    def from_dict(cls, data: dict) -> "storage_dto":
        """Фабричный метод создания корневого DTO хранилища"""
        if not isinstance(data, dict):
            return None
        return cls(
            warehouse=[warehouse_dto.from_dict(item) for item in data.get("warehouse", [])],
            unit=[unit_dto.from_dict(item) for item in data.get("unit", [])],
            group=[nomenclature_group_dto.from_dict(item) for item in data.get("group", [])],
            nomenclature=[nomenclature_dto.from_dict(item) for item in data.get("nomenclature", [])],
            recipe=[recipe_dto.from_dict(item) for item in data.get("recipe", [])]
        )