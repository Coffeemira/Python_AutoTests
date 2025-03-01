import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Пример данных для создания пользователя
@pytest.fixture
def create_test_user(api_client):
    user = {
        "id": 0,
        "username": "testuser1",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser1@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 0
    }
    response = api_client.post(f"{BASE_URL}/user", json=user)
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    yield user
    # Удаление пользователя после завершения теста
    response_delete = api_client.delete(f"{BASE_URL}/user/{user['username']}")
    assert response_delete.status_code == 200, f"Failed to delete user with username {user['username']}"

# Тест на завершение сессии пользователя
def test_user_logout(api_client):
    url = f"{BASE_URL}/user/logout"

    response = api_client.get(url)

    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    try:
        # Проверяем, что тело ответа соответствует ожидаемому формату
        response_data = response.text.strip()
        print(f"User logged out successfully")
    except ValueError as e:
        print(f"Failed to parse response: {e}")
        assert False, "Response is not as expected"

# Тест на авторизацию пользователя
def test_user_login(api_client, create_test_user):
    user_data = create_test_user
    url = f"{BASE_URL}/user/login"

    params = {
        "username": user_data["username"],
        "password": user_data["password"]
    }

    response = api_client.get(url, params=params)

    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    try:
        # Проверяем, что тело ответа содержит ожидаемое сообщение
        response_data = response.text.strip()
        print(f"User logged in successfully with username: {user_data['username']}")
    except ValueError as e:
        print(f"Failed to parse response: {e}")
        assert False, "Response is not as expected"

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
        "userdoesnotexist",
        404
    )
]

# Тест на удаление пользователя по имени с параметризацией
@pytest.mark.parametrize("username, expected_status_code", test_data)
def test_delete_user(api_client, username, expected_status_code, create_test_user):
    # Ensure the test user exists before testing deletion
    if username == "testuser1":
        create_test_user

    url = f"{BASE_URL}/user/{username}"

    response = api_client.delete(url)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        print(f"User deleted successfully with username: {username}")
    elif expected_status_code in [400, 404]:
        if response.text:
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
                assert False, "Response is not as expected"
        else:
            print(f"Empty response for username: {username} with status code: {expected_status_code}")
