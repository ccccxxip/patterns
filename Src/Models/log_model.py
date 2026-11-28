from datetime import datetime
from Src.Core.base_model import base_model
from Src.Core.constants import LOG_DATETIME_FORMAT
from Src.Core.event_type import event_type
from Src.Core.log_subsystem import log_subsystem
from Src.Dtos.log_type_enum import log_type_enum


class log_model(base_model):
    """
    Доменная модель записи журнала логирования
    Хранит информацию о событии, его уровне, источнике и времени возникновения
    """

    def __init__(
        self,
        subsystem: log_subsystem | str = log_subsystem.SYSTEM,
        level: log_type_enum | str = log_type_enum.INFO,
        event: event_type | str = event_type.API_REQUEST,
        message: str = "",
        period: datetime | None = None
    ) -> None:
        """
        Инициализация записи лога
        """
        super().__init__()
        self.__period: datetime = period if period is not None else datetime.now()
        self.__level: log_type_enum = level if isinstance(level, log_type_enum) else log_type_enum(level)
        self.__subsystem: log_subsystem = subsystem if isinstance(subsystem, log_subsystem) else log_subsystem(subsystem)
        self.__event: event_type = event if isinstance(event, event_type) else event_type(event)
        self.__message: str = str(message)
        self.name = f"[{self.__level.value}] {self.__subsystem.value}"

    @property
    def period(self) -> datetime:
        """Дата и время события"""
        return self.__period

    @property
    def level(self) -> log_type_enum:
        """Уровень логирования"""
        return self.__level

    @property
    def subsystem(self) -> log_subsystem:
        """Подсистема источника события"""
        return self.__subsystem

    @property
    def event(self) -> event_type:
        """Тип события"""
        return self.__event

    @property
    def message(self) -> str:
        """Текстовое сообщение лога"""
        return self.__message

    def __contains__(self, item: str) -> bool:
        """Проверка вхождения подстроки """
        return item in str(self)

    def __str__(self) -> str:
        """Форматированное строковое представление записи лога"""
        time_str = self.__period.strftime(LOG_DATETIME_FORMAT)
        event_str = getattr(self.__event, "value", str(self.__event)).upper()
        return f"[{time_str}] [{self.__level.value}] [{self.__subsystem.value.upper()}] [{event_str}] | {self.__message}"
