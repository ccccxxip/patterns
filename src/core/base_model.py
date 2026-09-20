from abc import ABC
import uuid


class base_model(ABC):
    # Класс для доменных сущностей

    def __init__(self) -> None:
        # Создаётся новая сущность с уникальным ID
        self._id: str = str(uuid.uuid4())
        self._name: str = ""

    @property
    def id(self) -> str:
        # Возвращает уникальный ID сущности
        return self._id

    @property
    def name(self) -> str:
        # Возвращает имя сущности
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        # Задаёт имя сущности
        if not isinstance(value, str):
            raise ValueError("Наименование должно быть строкой.")

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Наименование не может быть пустым.")

        self._name = normalized_value