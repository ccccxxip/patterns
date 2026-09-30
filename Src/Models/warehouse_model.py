from Src.Core.base_model import base_model


class warehouse_model(base_model):
    """ Модель "Склад" - место хранения номенклатуры """

    def __init__(self, name: str) -> None:
        """ Создаёт склад с указанным наименованием """
        super().__init__()
        self.name = name