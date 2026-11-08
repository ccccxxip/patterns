from abc import ABC, abstractmethod


class abstract_mapping_factory(ABC):
    """
    Базовый интерфейс фабрики маппинга
    """

    @abstractmethod
    def to_dto(self, source: object) -> object:
        """Сконвертировать доменную модель в Dto"""
        pass

    @abstractmethod
    def to_model(self, source: object) -> object:
        """Сконвертировать Dto в доменную модель"""
        pass