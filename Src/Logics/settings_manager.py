import json
from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator, operation_exception
from Src.Models.settings_model import settings_model
from Src.Models.organization_model import organization_model


class settings_manager(abstract_manager):
    """
    Менеджер настроек
    Отвечает за загрузку данных из JSON и их безопасное преобразование 
    в типизированную модель settings_model
    Реализует Singleton для обеспечения единой точки доступа к настройкам
    """

    __default_file_name: str = "Src/settings.json"
    __settings: settings_model = None
    __data: dict = {}

    def __init__(self):  
        """ 
        Инициализирует менеджер
        Если экземпляр модели настроек еще не создан — создает пустой объект settings_model
        """
        if self.__settings is None:
            self.__settings = settings_model()

    # Singleton 
    def __new__(cls):  
        """ 
        Если экземпляр уже существует, возвращает его вместо создания нового
        Гарантирует, что настройки читаются один раз и доступны везде
        """
        if not hasattr(cls, 'instance'):  
            cls.instance = super(settings_manager, cls).__new__(cls)  
        return cls.instance 

    def load(self, file_name: str = "") -> None:  
        """
        Загружает данные из JSON
        
        file_name: Путь к файлу. Если не передан или пуст, используется путь по умолчанию
        raises operation_exception: При ошибке чтения файла или неверном формате данных
        """
        
        # Если передали None или пустую строку (включ. пробелы) — путь по умолчанию
        if file_name is None or (isinstance(file_name, str) and not file_name.strip()):
            inner_file_name = self.__default_file_name
        else:
            # иначе оставляем как есть, ниже валидатор словит ошибки
            inner_file_name = file_name

        # валидация: гарантируем, что итоговый путь — это строка
        validator.validate(inner_file_name, str, field_name="file_name")

        try:  
            with open(inner_file_name, "r", encoding="utf-8") as file:  
                self.__data = json.load(file)
                self._is_loaded = self.convert()
        except Exception as ex:   
            raise operation_exception(f"Ошибка при загрузке и обработке файла: {inner_file_name}. Детали: {ex}")
    
    def convert(self) -> bool:
        """
        Переносит данные из черновика __data в чистую модель __settings
        Защищает от ситуаций, когда в JSON отсутствуют ключи
        """
        if not self.__data:
            return False

        # Загрузка организации. 
        # Если данные некорректны или неполны - ошибка не глушится, а поднимается через внешний try/except в load()
        if "organization" in self.__data:
            org_data = self.__data["organization"]
            self.__settings.organization = organization_model(
                name=org_data["name"],
                inn=org_data["inn"],
                bik=org_data["bik"],
                account=org_data["account"],
                ownership_form=org_data["ownership_form"]
            )

        # Если ключа нет, останется значение по умолчанию
        if "boss_name" in self.__data:
            self.__settings.boss_name = self.__data["boss_name"]

        if "account_name" in self.__data:
            self.__settings.account_name = self.__data["account_name"]

        if "is_first_start" in self.__data:
            self.__settings.is_first_start = bool(self.__data["is_first_start"])

        return True

    @property  
    def settings(self) -> settings_model:  
        """ 
        возвращает готовую модель настроек
        """
        return self.__settings