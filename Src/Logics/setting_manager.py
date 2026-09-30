import os
import json
from Src.Core.abstract_manager import abstract_manager
from Src.Core.exception import arguments_exception
from Src.Models.setting_model import settings_model


class settings_manager(abstract_manager):

    # Определяем путь к Src/settings.json относительно расположения данного файла (setting_manager.py)
    __cur_dir = os.path.dirname(os.path.abspath(__file__))  # Src/Logics
    __src_dir = os.path.dirname(__cur_dir)                 # Src
    __default_file_name: str = os.path.join(__src_dir, "settings.json")

    __settings: settings_model = None
    __data: dict = {}
    __is_loaded: bool = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def load(self, file_name: str = "") -> bool:
        inner_file_name = file_name if file_name.strip() != "" else self.__default_file_name
        self._load_validator(inner_file_name)

        try:
            with open(inner_file_name, "r", encoding="utf-8") as file:
                self.__data = json.load(file)
                self.__is_loaded = self.convert()
                return True
        except Exception as ex:
            raise arguments_exception("file_name", f"Ошибка чтения файла настроек: {ex}")

    def _load_validator(self, file_name: str = None) -> None:
        if file_name is not None and not isinstance(file_name, str):
            raise arguments_exception("file_name", "Имя файла должно быть строкой")

    def convert(self) -> bool:
        if self.__data:
            model = settings_model()
            model.load_from_dict(self.__data)
            self.__settings = model
            return True
        return False

    @property
    def settings(self) -> settings_model:
        return self.__settings

    @property
    def is_loaded(self) -> bool:
        return self.__is_loaded