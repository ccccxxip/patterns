from enum import Enum


class event_type(str, Enum):
    """
    Реестр типов системных событий
    """

    # Настройки
    CHANGE_SETTINGS = "change_settings"
    LOAD_SETTINGS = "load_settings"

    # CRUD операции
    CREATE_ENTITY = "create_entity"
    UPDATE_ENTITY = "update_entity"
    DELETE_ENTITY = "delete_entity"

    # Складские операции
    WAREHOUSE_TRANSACTION = "warehouse_transaction"

    # Web вызовы
    API_REQUEST = "api_request"

    # Методы доступа
    @classmethod
    def change_settings(cls) -> "event_type":
        """изменены настройки"""
        return cls.CHANGE_SETTINGS

    @classmethod
    def load_settings(cls) -> "event_type":
        """загружены настройки"""
        return cls.LOAD_SETTINGS

    @classmethod
    def create_entity(cls) -> "event_type":
        """создана сущность"""
        return cls.CREATE_ENTITY

    @classmethod
    def update_entity(cls) -> "event_type":
        """обновлена сущность"""
        return cls.UPDATE_ENTITY

    @classmethod
    def delete_entity(cls) -> "event_type":
        """удалена сущность"""
        return cls.DELETE_ENTITY

    @classmethod
    def warehouse_transaction(cls) -> "event_type":
        """складская операция"""
        return cls.WAREHOUSE_TRANSACTION

    @classmethod
    def api_request(cls) -> "event_type":
        """вызов Web-метода API"""
        return cls.API_REQUEST
