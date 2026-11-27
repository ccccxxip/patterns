import os
from datetime import datetime
from Src.Core.abstract_observer import abstract_observer
from Src.Core.constants import LOG_DATETIME_FORMAT, LOG_ENCODING, DEFAULT_LOG_PATH


class log_observer(abstract_observer):
    """
    Наблюдатель для логирования событий в файл
    """
    def __init__(self, log_file: str = DEFAULT_LOG_PATH):
        self.__log_file: str = log_file
        self.__ensure_directory()

    def __ensure_directory(self) -> None:
        """Создает директорию для лог-файла, если она не существует"""
        directory = os.path.dirname(self.__log_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    @property
    def log_file(self) -> str:
        """Путь к файлу лога"""
        return self.__log_file

    def __eq__(self, other: object) -> bool:
        """два логгера равны, если пишут в один файл"""
        if isinstance(other, log_observer):
            return self.__log_file == other.log_file
        return False

    def handler(self, event_types: str, params: object = None) -> None:
        """
        форматирование и сохранение в лог-файл
        """
        timestamp = datetime.now().strftime(LOG_DATETIME_FORMAT)
        param_str = f" | {params}" if params is not None else ""
        log_entry = f"[{timestamp}] [{event_types.upper()}]{param_str}\n"

        self.__ensure_directory()
        with open(self.__log_file, "a", encoding=LOG_ENCODING) as f:
            f.write(log_entry)
