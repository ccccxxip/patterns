"""
Кэш идентичности
Нужен для сохранения ссылочной целостности графа доменных сущностей
и исключения дублирования объектов в памяти при десериализации
"""

class identity_cache:
    """
    Реестр загруженных доменных сущностей по их id
    """
    def __init__(self):
        """Инициализация пустого словаря кэша"""
        self.__cache: dict = {}

    def get(self, entity_id: str, entity_type: str = "") -> object:
        """
        Получает доменный объект из кэша по идентификатору (и опционально типу)
        """
        if not entity_id:
            return None

        # Проверка по составному ключу (тип, id), если тип указан
        if entity_type:
            key = (entity_type, str(entity_id))
            if key in self.__cache:
                return self.__cache[key]

        # Прямой поиск по id
        return self.__cache.get(str(entity_id))

    def add(self, entity_id: str, entity: object, entity_type: str = "") -> None:
        """
        Регистрирует доменный объект в кэше
        """
        if not entity_id or entity is None:
            return

        str_id = str(entity_id)
        self.__cache[str_id] = entity
        if entity_type:
            self.__cache[(entity_type, str_id)] = entity

    def contains(self, entity_id: str) -> bool:
        """
        Проверяет, зарегистрирован ли уже объект с таким id в кэше
        """
        return str(entity_id) in self.__cache

    def clear(self) -> None:
        """
        Очищает кэш перед началом новой операции десериализации
        """
        self.__cache.clear()

    @property
    def count(self) -> int:
        """
        Возвращает количество уникальных доменных объектов в кэше
        """
        unique_objects = {id(obj) for obj in self.__cache.values()}
        return len(unique_objects)