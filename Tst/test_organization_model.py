from Src.Models.organization_model import organization_model
from Src.Core.exception import arguments_exception


def _valid_org(**overrides) -> organization_model:
    """Вспомогательная функция для генерации тестовой организации"""
    params = {
        "name": "ООО Ромашка",
        "inn": "7707083893",
        "bik": "044525225",
        "account": "40702810900000001234",
        "ownership_form": "ООО",
    }
    params.update(overrides)
    return organization_model(**params)


def test_create_organization_with_valid_data_returns_object():
    """
    Сценарий: создание организации с верными реквизитами (10-значный ИНН)
    Ожидаемый результат: объект нормально создается, все поля сохраняются
    """
    org = _valid_org()

    assert org.name == "ООО Ромашка"
    assert org.inn == "7707083893"
    assert org.bik == "044525225"
    assert org.account == "40702810900000001234"
    assert org.ownership_form == "ООО"


def test_create_organization_with_12_digit_inn_for_ip_returns_object():
    """
    Сценарий: создание ИП с ИНН из 12 цифр
    Ожидаемый результат: объект успешно создается с 12-значным ИНН
    """
    org = _valid_org(inn="123456789012", ownership_form="ИП")

    assert org.inn == "123456789012"


def test_create_organization_with_invalid_inn_length_raises_arguments_exception():
    """
    Сценарий: передача ИНН с неверным количеством цифр
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False

    try:
        _valid_org(inn="123")
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_create_organization_with_non_digit_inn_raises_arguments_exception():
    """
    Сценарий: передача ИНН, в котором есть буквы
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False

    try:
        _valid_org(inn="77070838a3")
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_create_organization_with_invalid_bik_length_raises_arguments_exception():
    """
    Сценарий: передача БИК неверной длины (не 9 цифр)
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False

    try:
        _valid_org(bik="12345")
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_create_organization_with_invalid_account_length_raises_arguments_exception():
    """
    Сценарий: передача расчетного счета не из 20 цифр
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False

    try:
        _valid_org(account="12345")
    except arguments_exception:
        is_exception = True

    assert is_exception is True


def test_create_organization_with_empty_ownership_form_raises_arguments_exception():
    """
    Сценарий: передача пустой строки в форму собственности
    Ожидаемый результат: выбрасывается исключение arguments_exception
    """
    is_exception = False

    try:
        _valid_org(ownership_form="")
    except arguments_exception:
        is_exception = True

    assert is_exception is True