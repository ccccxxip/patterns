class reference_index:
    """
    Обратный индекс ссылочной целостности доменных сущностей
    """
    def __init__(self):
        # Словарь: target_id -> list[str] (список сущностей-зависимостей)
        self.__index: dict = {}

    def build(self, data: dict) -> None:
        """Перебрасывает коллекции сущностей в обратный индекс зависимостей"""
        self.__index.clear()
        
        # Индексируем связи единиц измерения
        for u in data.get("unit", []):
            if u.base_unit and str(u.base_unit.id) != str(u.id):
                self._add(u.base_unit.id, f"Единица измерения '{u.name}' использует её как базовую единицу")

        # Индексируем связи номенклатуры
        for n in data.get("nomenclature", []):
            if n.group:
                self._add(n.group.id, f"Номенклатура '{n.name}' входит в эту группу")
            if n.unit:
                self._add(n.unit.id, f"Номенклатура '{n.name}' использует эту единицу измерения")

        # Индексируем связи рецептов
        for r in data.get("recipe", []):
            if r.owner:
                self._add(r.owner.id, f"Рецепт '{r.name}' привязан к этой номенклатуре как владелец")
            for ing in getattr(r, "ingredients", []):
                if ing.unit:
                    self._add(ing.unit.id, f"Рецепт '{r.name}' использует эту единицу измерения в ингредиенте '{ing.name}'")
                if ing.nomenclature:
                    self._add(ing.nomenclature.id, f"Рецепт '{r.name}' использует эту номенклатуру в ингредиенте '{ing.name}'")
                if getattr(ing, "recipe", None) and str(ing.recipe.id) != str(r.id):
                    self._add(ing.recipe.id, f"Рецепт '{r.name}' включает этот рецепт как полуфабрикат")

    def _add(self, target_id: str, description: str):
        tid = str(target_id).strip()
        if tid not in self.__index:
            self.__index[tid] = []
        self.__index[tid].append(description)

    def get_relations(self, target_id: str) -> list:
        """ Поиск связей"""
        return self.__index.get(str(target_id).strip(), [])