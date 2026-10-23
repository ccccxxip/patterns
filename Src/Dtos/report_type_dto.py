from enum import Enum

""" типы отчетов"""
class report_type_enum(Enum):
    """текстовый формат"""
    TXT = 1 
    """формат CSV"""
    CSV = 2
    """формат Markdown"""
    MARKDOWN = 3
    """формат XML"""
    XML = 4
    """формат HTML"""
    HTML = 5
