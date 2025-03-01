import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Валидные данные для авторизации
valid_users_data = [
    {
        "username": "testuser1",
        "password": "password123"
    },
    {
        "username": "testuser2",
        "password": "password123"
    }
]

# Невалидные данные для авторизации
invalid_users_data = [
    {
        "username": "invaliduser",
        "password": "wrongpassword"
    }
]

# Тестовые данные: валидные и невалидные
test_data = [
    # Валидные данные
    *[(user["username"], user["password"], 200) for user in valid_users_data],
    # Невалидные данные
    *[(user["username"], user["password"], 400) for user in invalid_users_data]
]


# Тест на авторизацию пользователя с параметризацией
@pytest.mark.parametrize("username, password, expected_status_code", test_data)
def test_user_login(api_client, username, password, expected_status_code):
    url = f"{BASE_URL}/user/login"

    params = {
        "username": username,
        "password": password
    }

    response = api_client.get(url, params=params)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        try:
            # Проверяем, что тело ответа содержит ожидаемое сообщение
            response_data = response.text.strip()
            print(f"User logged in successfully with username: {username}")
        except ValueError as e:
            print(f"Failed to parse response: {e}")
            assert False, "Response is not as expected"
    elif expected_status_code == 400:
        try:
            # Проверяем, что тело ответа содержит сообщение об ошибке
            error_message = response.text.strip()
            assert error_message, "Error message should be present in the response"
            print(f"Error message: {error_message}")
        except ValueError as e:
            print(f"Failed to parse response: {e}")
            assert False, "Response is not as expected"

