import pytest

from rest_framework.exceptions import ValidationError

from users.validators.password import validate_password_policy


def test_valid_password():
    assert validate_password_policy("ValidPass159") == "ValidPass159"

def test_too_short_password():
    with pytest.raises(ValidationError) as e:
        validate_password_policy("abc")
    assert "at least 8 characters" in str(e.value)

@pytest.mark.parametrize("password", [
    "12345678",     # 숫자만
    "password",     # 소문자만
    "PASSWORD",     # 대문자만
    "abcdefghi",    # 소문자만
])
def test_insufficient_combination(password):
    with pytest.raises(ValidationError) as e:
        validate_password_policy(password)
    assert "at least 2 types" in str(e.value)

@pytest.mark.parametrize("password", [
    "testpassword111",     # 숫자 반복
    "aaapassword159",     # 문자 반복
    "aaapassword111"    # 숫자, 문자 반복
])
def test_repeated_characters(password):
    with pytest.raises(ValidationError) as e:
        validate_password_policy(password)
    assert "same character 3 times" in str(e.value)

@pytest.mark.parametrize("password", [
    "testpassword123",     # 연속 숫자
    "abcpassword159",     # 연속 문자
    "abcpassword123"    # 연속 숫자, 문자
])
def test_consecutive_characters(password):
    with pytest.raises(ValidationError) as e:
        validate_password_policy(password)
    assert "3 or more consecutive characters" in str(e.value)
