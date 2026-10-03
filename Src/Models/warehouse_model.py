from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception


class warehouse_model(base_model):
    """ Модель "Склад" - место хранения номенклатуры """

    def __init__(self, name: str, address: str) -> None:
        """ 
        Создаёт склад с указанным наименованием и адресом 
        
        name: Наименование склада (валидируется в base_model)
        address: Адрес склада
        """
        super().__init__()
        self.name = name
        self.address = address

    @property
    def address(self) -> str:
        """Возвращает адрес склада"""
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        """
        Задаёт адрес склада
        """
        if not isinstance(value, str):
            raise arguments_exception("address", "Адрес должен быть строкой")
            
        normalized_value = value.strip()
        
        if not normalized_value:
            raise arguments_exception("address", "Адрес не может быть пустым")
            
        self._address = normalized_value