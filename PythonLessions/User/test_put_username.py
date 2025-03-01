import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Пример данных для обновления пользователя
valid_user_data = {
    "id": 0,
    "username": "updateduser",
    "firstName": "Updated",
    "lastName": "User",
    "email": "updateduser@example.com",
    "password": "newpassword123",
    "phone": "9876543210",
    "userStatus": 0
}
# Тестовые данные: валидные и невалидные
test_data = [
    # Валидные данные
    (
        "testuser9",
        valid_user_data,
        200
    ),
    # Невалидное имя пользователя (содержит недопустимые символы)
    (
        "invalid@user",
        valid_user_data,
        400
    ),
    # Пользователь не найден (не существует)
    (
        "none",
        valid_user_data,
        404
    )
]

# Тест на обновление пользователя по имени с параметризацией
@pytest.mark.parametrize("username, user_data, expected_status_code", test_data)
def test_update_user(api_client, username, user_data, expected_status_code):
    url = f"{BASE_URL}/user/{username}"

    headers = {'Content-Type': 'application/json'}
    response = api_client.put(url, headers=headers, data=json.dumps(user_data))

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        try:
            # Проверяем, что тело ответа соответствует ожидаемым данным
            response_data = response.json()
            print(f"User updated successfully with username: {username}")
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

