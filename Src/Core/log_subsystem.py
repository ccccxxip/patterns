from enum import Enum


class log_subsystem(str, Enum):
    """
    Перечисление подсистем приложения для категоризации событий логирования
    """
    SETTINGS = "Settings"
    STORAGE = "Storage"
    CRUD = "CRUD"
    WEB = "Web"
    SYSTEM = "System"
