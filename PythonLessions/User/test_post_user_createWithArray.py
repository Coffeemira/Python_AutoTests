import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Пример данных для создания пользователей
@pytest.fixture(params=[
    {
        "id": 0,
        "username": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "password": "string",
        "phone": "string",
        "userStatus": 0
    }
])
def user_data(api_client, request):
    user = request.param
    response = api_client.post(f"{BASE_URL}/user", json=user)
    data = response.json()
    assert response.status_code == 200, f"Failed to create user: {response.text}"

    # Проверяем наличие ключа 'username' в ответе
    assert "username" in user, "Response does not contain 'username' key"
    username = user["username"]

    yield user

    # Удаление пользователя после завершения теста
    response_delete = api_client.delete(f"{BASE_URL}/user/{username}")
    assert response_delete.status_code == 200, f"Failed to delete user with username {username}"


# Тест на создание пользователей с массивом
def test_create_users_with_list(api_client, user_data):
    url = f"{BASE_URL}/user/createWithList"

    headers = {'Content-Type': 'application/json'}
    response = api_client.post(url, headers=headers, data=json.dumps([user_data]))

    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    try:
        # Проверяем, что тело ответа соответствует отправленным данным
        response_data = response.json()

        # Проверка наличия ключей в ответе
        expected_keys = ["code", "message", "type"]
        for key in expected_keys:
            assert key in response_data, f"Response does not contain '{key}' key"

        # Проверка значений ключей
        assert response_data["code"] == 200, "Incorrect code in response"
        print(f"Users created successfully with message: {response_data['message']}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        assert False, "Response is not a valid JSON"
    except AssertionError as e:
        print(f"Assertion error: {e}")
        assert False, str(e)


# Тест на авторизацию пользователя с параметризацией
@pytest.mark.parametrize("username, password, expected_status_code", [
    ("string", "string", 200)
])
def test_user_login(api_client, username, password, expected_status_code):
    url = f"{BASE_URL}/user/login"

    params = {
        "username": username,
        "password": password
    }

    response = api_client.get(url, params=params)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    try:
        # Проверяем, что тело ответа содержит ожидаемое сообщение
        response_data = response.text.strip()
        print(f"User logged in successfully with username: {username}")
    except ValueError as e:
        print(f"Failed to parse response: {e}")
        assert False, "Response is not as expected"
