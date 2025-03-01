import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тестовые данные: валидные и невалидные
test_data = [
    # Валидное имя пользователя
    (
        "testuser",
        200
    ),
    # Невалидное имя пользователя (содержит недопустимые символы)
    (
        "invalid@user",
        400
    ),
    # Пользователь не найден (не существует)
    (
        "nonexistentuser",
        404
    )
]

# Тест на получение пользователя по имени с параметризацией
@pytest.mark.parametrize("username, expected_status_code", test_data)
def test_get_user_by_username(api_client, username, expected_status_code):
    url = f"{BASE_URL}/user/{username}"

    response = api_client.get(url)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        try:
            # Проверяем, что тело ответа содержит ожидаемые данные
            response_data = response.json()
            assert response_data["username"] == username, "Incorrect username in response"
            print(f"User retrieved successfully with username: {response_data['username']}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
    elif expected_status_code in [400, 404]:
        try:
            # Проверяем, что тело ответа содержит сообщение об ошибке
            error_message = response.json().get("message")
            assert error_message is not None, "Error message should be present in the response"
            print(f"Error message: {error_message}")
        except ValueError as e:
            # Если ответ не является JSON, проверяем, что он не пустой
            if not response.text:
                assert False, "Empty response for error status code"
            else:
                print(f"Non-JSON error response: {response.text}")
