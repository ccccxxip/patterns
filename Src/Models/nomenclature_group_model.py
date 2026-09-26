from Src.Core.base_model import base_model


class nomenclature_group_model(base_model):
    """
    Модель данных "Группа номенклатуры"
    Наследуется от base_model
    """

    def __init__(self, name: str) -> None:
        """
        Инициализирует экземпляр группы номенклатуры

        name: Наименование группы номенклатуры (валидируется в base_model)
        """
        super().__init__()
        self.name = name