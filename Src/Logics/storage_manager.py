from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator
from Src.Logics.settings_manager import settings_manager

from Src.Models.warehouse_model import warehouse_model 
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_model import nomenclature_model


class storage_manager(abstract_manager):
    """
    Менеджер хранилища данных (бд в оперативной памяти)
    Singleton для обеспечения единой точки доступа к сущностям
    Отвечает за первичное наполнение данных при первом запуске программы
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
                "nomenclature": []
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
            
            # Единицы измерения

            # Вес
            g = unit_model("Грамм", 1)
            self.add("unit", g)
    
            kg = unit_model("Кг", 1000, g)
            self.add("unit", kg)
            
            # Объем
            ml = unit_model("Миллилитр", 1)
            self.add("unit", ml)
            
            l = unit_model("Литр", 1000, ml)
            self.add("unit", l)
            
            # Штуки
            pcs = unit_model("Штука", 1)
            self.add("unit", pcs)
    
            # Группы номенклатуры
            ingredients = nomenclature_group_model("Ингредиенты")
            self.add("group", ingredients)

            # Склады
            main_warehouse = warehouse_model("Основной склад", "ул. Гагарина, д. 101")
            self.add("warehouse", main_warehouse)

            # Номенклатура
            flour = nomenclature_model("Мука", "Мука пшеничная высший сорт", ingredients, kg)
            self.add("nomenclature", flour)

            sugar = nomenclature_model("Сахар", "Сахар-песок белый", ingredients, kg)
            self.add("nomenclature", sugar)

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