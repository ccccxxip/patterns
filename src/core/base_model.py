from abc import ABC
import uuid
from Src.Core.constants import NAME_MAX_LENGTH
from Src.Core.exception import arguments_exception


class base_model(ABC):
    """ Базовый абстрактный класс для всех доменных моделей """

    def __init__(self) -> None:
        """ Инициализирует базовую модель с уникальным идентификатором и пустым именем """
        self._id: str = str(uuid.uuid4())
        self._name: str = ""

    @property
    def id(self) -> str:
        """ Возвращает уникальный идентификатор сущности """
        return self._id

    @id.setter
    def id(self, value: str) -> None:

        """
        Задаёт уникальный идентификатор сущности

        raises arguments_exception: Если передан неверный тип или пустая строка
        """

        if not isinstance(value, str):
            raise arguments_exception("id", "ID должен быть строкой.")

        normalized_value = value.strip()

        if not normalized_value:
            raise arguments_exception("id", "ID не может быть пустым.")

        self._id = normalized_value

    @property
    def name(self) -> str:
        """ Возвращает наименование сущности """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        
        """
        Задаёт наименование сущности
        
        raises arguments_exception: Если передан неверный тип, пустая строка или длина превышает допустимую
        """

        if not isinstance(value, str):
            raise arguments_exception("name", "Наименование должно быть строкой.")

        normalized_value = value.strip()

        if not normalized_value:
            raise arguments_exception("name", "Наименование не может быть пустым.")

        if len(normalized_value) > NAME_MAX_LENGTH:
            raise arguments_exception(
                "name",
                f"Наименование не может превышать {NAME_MAX_LENGTH} символов.",
            )

        self._name = normalized_value

    def __eq__(self, other: object) -> bool:
        """ Проверяет равенство объектов по их уникальному идентификатору """
        if not isinstance(other, base_model):
            return False
        return self.id == other.id