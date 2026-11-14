import json
from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator, operation_exception
from Src.Models.settings_model import settings_model
from Src.Models.organization_model import organization_model
from Src.Dtos.report_type_dto import report_type_enum


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
        raises operation_exception: При ошибке чтения файла (файл не найден, битый JSON и т.д.)
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
        Переносит данные из __data в чистую модель __settings 
        через общий механизм десериализации (mapping_factory)
        """
        if not self.__data:
            return False

        from Src.Logics.mapping_factory import mapping_factory

        try:
            factory = mapping_factory()
            model = factory.deserialize("settings", self.__data)
            if model is not None:
                self.__settings = model

            # Если блок organization был передан в JSON, но не распарсился
            if "organization" in self.__data and self.__data["organization"] is not None and model.organization is None:
                return False

            return True
        except Exception:
            return False
    @property  
    def settings(self) -> settings_model:  
        """ 
        возвращает готовую модель настроек
        """
        return self.__settings