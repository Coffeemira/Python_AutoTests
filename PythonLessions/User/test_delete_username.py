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
        "testuser1",
        200
    ),
    # Невалидное имя пользователя (содержит недопустимые символы)
    (
        "invalid@user",
        400
    ),
    # Пользователь не найден (не существует)
    (
        "none",
        404
    )
]

# Тест на удаление пользователя по имени с параметризацией
@pytest.mark.parametrize("username, expected_status_code", test_data)
def test_delete_user(api_client, username, expected_status_code):
    url = f"{BASE_URL}/user/{username}"

    response = api_client.delete(url)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        print(f"User deleted successfully with username: {username}")
    elif expected_status_code in [400, 404]:
        try:
            # Проверяем, что тело ответа соответствует отправленным данным
            response_data = response.json()
            if "message" in response_data:
                error_message = response_data.get("message")
                assert error_message is not None, "Error message should be present in the response"
                print(f"Error message: {error_message}")
            else:
                print("Response does not contain 'message' key")
                assert False, "Response is missing the 'message' key"
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            if not response.text:
                print("Empty response for error status code")
                assert False, "Empty response for error status code"
            else:
                print(f"Non-JSON error response: {response.text}")

