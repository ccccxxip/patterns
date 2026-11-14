from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception


class nomenclature_group_model(base_model):
    """
    Доменная модель: "Группа номенклатуры"
    Наследуется от base_model
    Служит для категоризации складских остатков и рецептов по папкам
    """

    def __init__(self, name: str) -> None:
        """
        Инициализирует экземпляр группы номенклатуры.

        name: Наименование группы номенклатуры
        """
        super().__init__()
        self.name = name



    @staticmethod
    def create_ingredients() -> "nomenclature_group_model":
        """ Фабричный метод: группа "Ингредиенты" (базовые составляющие, не требующие готовки) """
        return nomenclature_group_model("Ингредиенты")

    @staticmethod
    def create_raw() -> "nomenclature_group_model":
        """ Фабричный метод: группа "Сырье" (мясо, овощи, бакалея) """
        return nomenclature_group_model("Сырье")

    @staticmethod
    def create_semi_finished() -> "nomenclature_group_model":
        """ 
        Фабричный метод: группа "Полуфабрикаты"
        Сюда попадают результаты работы промежуточных рецептов (Сливочно-грибной соус)
        """
        return nomenclature_group_model("Полуфабрикаты")

    @staticmethod
    def create_packaging() -> "nomenclature_group_model":
        """ 
        Фабричный метод: группа "Упаковка"
        Отдельная группа для несъедобной тары (контейнер)
        """
        return nomenclature_group_model("Упаковка")

    @staticmethod
    def create_finished() -> "nomenclature_group_model":
        """ 
        Фабричный метод: группа "Готовая продукция"
        Сюда сохраняются финальные блюда (Паста)
        """
        return nomenclature_group_model("Готовая продукция")
    
    @classmethod
    def create(cls, data: dict) -> "nomenclature_group_model":
        """
        Фабричный метод создания группы номенклатуры из словаря данных
        """
        if not isinstance(data, dict):
            raise arguments_exception("data", "Ожидался словарь данных")

        name = data.get("name", "")
        item = cls(name=name)

        if data.get("id"):
            item.id = data["id"]

        return item