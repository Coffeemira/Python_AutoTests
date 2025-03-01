import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания пользователя
@pytest.fixture
def create_user(api_client):
    user_data = {
        "id": 0,
        "username": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "password": "string",
        "phone": "string",
        "userStatus": 0
    }
    response = api_client.post(f'{BASE_URL}/user', json=user_data)
    data = response.json()
    username = user_data['username']
    yield username
    # Удаление пользователя после завершения теста
    response_delete = api_client.delete(f'{BASE_URL}/user/{username}')
    assert response_delete.status_code == 200, f"Failed to delete user with username {username}"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Положительный тест на успешный запрос получения пользователя
def test_get_user_success(api_client, create_user):
    url = f"{BASE_URL}/user/{create_user}"
    response = api_client.get(url)
    assert response.status_code == 200

    try:
        # Проверяем, что тело ответа содержит ожидаемые данные
        response_data = response.json()
        assert response_data["username"] == create_user, "Incorrect username in response"
        assert response_data["firstName"] == "string", "Incorrect first name in response"
        assert response_data["lastName"] == "string", "Incorrect last name in response"
        assert response_data["email"] == "string", "Incorrect email in response"
        assert response_data["phone"] == "string", "Incorrect phone in response"
        assert response_data["userStatus"] == 0, "Incorrect user status in response"
        print(f"User retrieved successfully with username: {response_data['username']}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        assert False, "Response is not a valid JSON"
    except AssertionError as e:
        print(f"Assertion error: {e}")
        assert False, str(e)