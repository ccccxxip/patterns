from abc import ABC

"""
Абстрактный класс для реализации загрузки и обработки данных 
"""
class abstract_manager(ABC):
    # Полный путь к файлу
    __file_name:str = ""
    # Флаг. Загрузка и обработка завершения успешно 
    __is_loaded:bool = False
    __data:list = []

    def load(self, file_name:str = "") -> None:
        pass

    def convert(self) -> bool:
        return False

    @property
    def is_loaded(self) -> bool:
        return self.__is_loaded