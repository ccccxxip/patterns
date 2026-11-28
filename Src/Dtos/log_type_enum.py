from enum import Enum


class log_type_enum(str, Enum):
    """
    Перечисление уровней важности сообщений логирования
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
