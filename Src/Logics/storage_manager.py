from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator
from Src.Logics.settings_manager import settings_manager

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

        return True

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