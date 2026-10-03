from Src.Core.validator import validator
from Src.Core.exception import arguments_exception


def test_validate_with_valid_string_type_returns_true():
    """
    Проверка, что передача корректного типа данных проходит успешно
    """
    # Подготовка
    test_value = "Тестовая строка"
    expected_type = str
    
    # Действие
    result = validator.validate(test_value, expected_type)
    
    # Проверка
    assert result is True


def test_validate_with_invalid_type_raises_arguments_exception():
    """
    Проверка, что передача неверного типа (число вместо строки) вызывает ошибку
    """
    # Подготовка
    test_value = 12345
    expected_type = str
    is_raised = False
    
    # Действие
    try:
        validator.validate(test_value, expected_type)
    except arguments_exception:
        is_raised = True
        
    # Проверка
    assert is_raised is True


def test_validate_with_valid_length_returns_true():
    """
    Проверка, что передача строки нужной длины проходит успешно
    """
    # Подготовка
    test_value = "12345"
    expected_type = str
    expected_length = 5
    
    # Действие
    result = validator.validate(test_value, expected_type, expected_length)
    
    # Проверка
    assert result is True


def test_validate_with_invalid_length_raises_arguments_exception():
    """
    Проверка, что передача строки, превышающей лимит длины, вызывает ошибку
    """
    # Подготовка
    test_value = "123456" 
    expected_type = str
    expected_length = 5    # Лимит 
    is_raised = False
    
    # Действие
    try:
        validator.validate(test_value, expected_type, expected_length)
    except arguments_exception:
        is_raised = True
        
    # Проверка
    assert is_raised is True