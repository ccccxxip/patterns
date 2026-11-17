from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator, operation_exception
from Src.Logics.settings_manager import settings_manager
from Src.Logics.reference_index import reference_index

from Src.Models.warehouse_model import warehouse_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model


class storage_manager(abstract_manager):
    """
    Менеджер хранилища данных (бд в оперативной памяти)
    Singleton для обеспечения единой точки доступа к сущностям
    Отвечает за первичное наполнение данных при первом запуске программы
    Все стартовые объекты создаются через фабричные методы доменных моделей
    """

    __data: dict = None

    def __new__(cls):
        """
        Singleton: гарантирует создание только одного экземпляра хранилища
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(storage_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """
        Инициализация словарей хранилища при первом создании объекта.
        """
        if self.__data is None:
            self.__data = {
                "warehouse": [],
                "unit": [],
                "group": [],
                "nomenclature": [],
                "recipe": []
            }
            self.__ref_index = reference_index()

    def load(self, file_name: str = "") -> None:
        """
        сразу делегирует работу методу генерации данных
        """
        self._is_loaded = self.convert()

    def convert(self) -> bool:
        """
        Бизнес-логика первого старта
        Генерирует стартовый набор, если в настройках активен флаг is_first_start.
        """
        set_mgr = settings_manager()

        if set_mgr.settings is not None and set_mgr.settings.is_first_start:

            # Единицы измерения (фабричные методы unit_model)
            # Производные единицы создаются от базовых, которые уже лежат в хранилище

            # Вес
            g = unit_model.create_gram()
            kg = unit_model.create_kilogram(g)
            tsp = unit_model.create_teaspoon(g)

            # Объем
            ml = unit_model.create_milliliter()
            l = unit_model.create_liter(ml)
            tbsp = unit_model.create_tablespoon(ml)

            # Штуки
            pcs = unit_model.create_piece()

            for unit in (g, kg, tsp, ml, l, tbsp, pcs):
                self.add("unit", unit)

            # Группы номенклатуры (фабричные методы nomenclature_group_model)
            ingredients = nomenclature_group_model.create_ingredients()
            raw = nomenclature_group_model.create_raw()
            semi = nomenclature_group_model.create_semi_finished()
            packaging = nomenclature_group_model.create_packaging()
            finished = nomenclature_group_model.create_finished()

            for group in (ingredients, raw, semi, packaging, finished):
                self.add("group", group)

            # Склады
            main_warehouse = warehouse_model("Основной склад", "ул. Гагарина, д. 101")
            self.add("warehouse", main_warehouse)

            # Номенклатура (фабричные методы nomenclature_model, тип задается методом)
            flour = nomenclature_model.create_product("Мука", "Мука пшеничная высший сорт", ingredients, kg)
            sugar = nomenclature_model.create_product("Сахар", "Сахар-песок белый", ingredients, kg)

            chicken = nomenclature_model.create_product("Куриное филе", "Куриное филе охл.", raw, g)
            mushrooms = nomenclature_model.create_product("Шампиньоны свежие", "Шампиньоны свежие", raw, g)
            cream = nomenclature_model.create_product("Сливки 20%", "Сливки 20%", raw, l)
            oil = nomenclature_model.create_product("Масло растительное", "Масло растительное", raw, tbsp)
            garlic = nomenclature_model.create_product("Чеснок", "Чеснок", raw, g)
            salt = nomenclature_model.create_product("Соль", "Соль пищевая", raw, tsp)
            pasta = nomenclature_model.create_product("Паста (феттуччине)", "Паста (феттуччине)", raw, g)
            parmesan = nomenclature_model.create_product("Сыр Пармезан", "Сыр Пармезан", raw, g)

            sauce = nomenclature_model.create_semi_finished("Сливочно-грибной соус", "Сливочно-грибной соус (п/ф)", semi, g)
            box = nomenclature_model.create_packaging("Контейнер крафтовый", "Контейнер крафтовый", packaging, pcs)
            dish = nomenclature_model.create_product("Паста сливочная с курицей", "Паста сливочная с курицей", finished, pcs)

            for item in (flour, sugar, chicken, mushrooms, cream, oil, garlic, salt, pasta, parmesan, sauce, box, dish):
                self.add("nomenclature", item)

            # Рецепты (фабричные методы recipe_model)
            sauce_recipe = recipe_model.create_sauce_recipe(sauce, chicken, mushrooms, cream, oil, garlic, salt)
            pasta_recipe = recipe_model.create_pasta_recipe(dish, pasta, sauce_recipe, parmesan, box, g)

            self.add("recipe", sauce_recipe)
            self.add("recipe", pasta_recipe)

            # Отключаем флаг, чтобы не дублировать данные при следующих запусках
            set_mgr.settings.is_first_start = False

        self.rebuild_index()
        return True

    def rebuild_index(self) -> None:
        """Перестроить обратный индекс ссылочной целостности"""
        if not hasattr(self, "_storage_manager__ref_index") or self.__ref_index is None:
            self.__ref_index = reference_index()
        self.__ref_index.build(self.__data)

    def add(self, key: str, item) -> None:
        """
        Безопасное добавление элемента в справочник с защитой от дубликатов

        key: Название справочника (ключ словаря __data)
        item: Добавляемый объект доменной модели
        """
        validator.validate(key, str, field_name="key")

        if key not in self.__data:
            self.__data[key] = []

        if item not in self.__data[key]:
            self.__data[key].append(item)

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def warehouses(self) -> list:
        return self.__data["warehouse"]

    @property
    def units(self) -> list:
        return self.__data["unit"]

    @property
    def groups(self) -> list:
        return self.__data["group"]

    @property
    def nomenclatures(self) -> list:
        return self.__data["nomenclature"]

    @property
    def recipes(self) -> list:
        return self.__data["recipe"]
        
    @staticmethod
    def normalize_key(key: str) -> str:
        """Приводит ключ сущности к стандартному виду (убирает _model, суффиксы и тд)"""
        k = str(key).lower().strip().replace("_model", "")
        aliases = {
            "warehouses": "warehouse",
            "units": "unit",
            "groups": "group",
            "nomenclatures": "nomenclature",
            "recipes": "recipe",
        }
        return aliases.get(k, k)

    def get_entities_by_type(self, entity_type: str) -> list:
        """Возвращает список всех сущностей указанного типа"""
        if not self.is_loaded:
            self.load()
        k = self.normalize_key(entity_type)
        return self.__data.get(k, [])

    def get_entity(self, entity_type: str, entity_id: str):
        """Ищет сущность по типу и id (или имени)"""
        items = self.get_entities_by_type(entity_type)
        target = str(entity_id).strip()
        for item in items:
            owner_name = getattr(item, "owner", None) and getattr(item.owner, "name", None)
            if getattr(item, "id", None) == target or getattr(item, "name", None) == target or owner_name == target:
                return item
        return None

    def check_relations(self, entity_type: str, item_id: str) -> list:
        """
        Проверяет ссылочную целостность через обратный индекс
        Возвращает список текстовых описаний найденных связей
        """
        if not self.is_loaded:
            self.load()

        if not hasattr(self, "_storage_manager__ref_index") or self.__ref_index is None:
            self.__ref_index = reference_index()
            self.rebuild_index()

        return self.__ref_index.get_relations(item_id)

    def add_entity(self, entity_type: str, item) -> object:
        """
        Добавляет доменную сущность с проверкой уникальности id
        """
        if not self.is_loaded:
            self.load()

        k = self.normalize_key(entity_type)
        if k not in self.__data:
            raise operation_exception(f"Неизвестный тип сущности: '{entity_type}'")

        item_id = getattr(item, "id", None)
        if item_id:
            for existing in self.__data[k]:
                if getattr(existing, "id", None) == item_id:
                    raise operation_exception(f"Сущность типа '{k}' с id '{item_id}' уже существует")

        self.add(k, item)
        self.rebuild_index()
        return item

    def delete_entity(self, entity_type: str, item_id: str) -> bool:
        """
        Удаляет доменную сущность с контролем ссылочной целостности
        """
        if not self.is_loaded:
            self.load()

        k = self.normalize_key(entity_type)
        if k not in self.__data:
            raise operation_exception(f"Неизвестный тип сущности: '{entity_type}'")

        existing = self.get_entity(k, item_id)
        if existing is None:
            raise operation_exception(f"Сущность типа '{k}' с id '{item_id}' не найдена")

        # Контроль связей: запрещено удалять, если есть зависимости
        relations = self.check_relations(k, existing.id)
        if relations:
            reasons = "; ".join(relations)
            raise operation_exception(
                f"Запрещено удалять сущность '{k}' с id '{item_id}', так как она связана с другими объектами: {reasons}"
            )

        self.__data[k].remove(existing)
        self.rebuild_index()
        return True

    def update_entity(self, entity_type: str, item_id: str, new_item) -> object:
        """
        Обновляет сущность. Если изменяется уникальный код (id), проверяет отсутствие связе
        """
        if not self.is_loaded:
            self.load()

        k = self.normalize_key(entity_type)
        if k not in self.__data:
            raise operation_exception(f"Неизвестный тип сущности: '{entity_type}'")

        existing = self.get_entity(k, item_id)
        if existing is None:
            raise operation_exception(f"Сущность типа '{k}' с id '{item_id}' не найдена")

        new_id = getattr(new_item, "id", item_id)
        # Если пытаются изменить ID сущности
        if new_id != item_id:
            relations = self.check_relations(k, item_id)
            if relations:
                reasons = "; ".join(relations)
                raise operation_exception(
                    f"Запрещено изменять код (id) сущности '{item_id}', так как она связана с другими объектами: {reasons}"
                )

        # Заменяем старый объект на новый
        idx = self.__data[k].index(existing)
        self.__data[k][idx] = new_item
        self.rebuild_index()
        return new_item