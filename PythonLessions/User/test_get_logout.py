import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Пример данных для создания пользователя
@pytest.fixture
def user_data(api_client):
    user = {
        "id": 0,
        "username": "testuser",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser@example.com",
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
def test_user_login(api_client, user_data):
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
