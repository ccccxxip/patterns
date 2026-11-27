"""
Модуль глобальных констант приложения
Содержит ограничения длины и валидационные параметры для доменных моделей
"""

# Максимальная допустимая длина короткого наименования сущности (base_model и дочерние модели)
NAME_MAX_LENGTH: int = 50

# Максимальная допустимая длина полного наименования (nomenclature_model)
FULL_NAME_MAX_LENGTH: int = 255

# Допустимые длины ИНН: 10 цифр — для юридических лиц, 12 цифр — для ИП (organization_model)
INN_VALID_LENGTHS: tuple[int, int] = (10, 12)

# Точная длина банковского идентификационного кода (organization_model)
BIK_LENGTH: int = 9

# Точная длина номера расчетного счета организации (organization_model)
ACCOUNT_LENGTH: int = 20

# Ключ словаря хранилища для складских транзакций
TRANSACTION_KEY: str = "transaction"

# Формат отметки времени в лог-файле
LOG_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

# Кодировка лог-файла
LOG_ENCODING: str = "utf-8"

# Путь по умолчанию к лог-файлу
DEFAULT_LOG_PATH: str = "Logs/app.log"
