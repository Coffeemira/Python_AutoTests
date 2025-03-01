import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Фикстура для данных пользователей
@pytest.fixture(params=[
    {
        "id": 0,
        "username": "testuser1",
        "firstName": "Test1",
        "lastName": "User1",
        "email": "testuser1@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 0
    },
    {
        "id": 1,
        "username": "testuser2",
        "firstName": "Test2",
        "lastName": "User2",
        "email": "testuser2@example.com",
        "password": "password123",
        "phone": "1234567891",
        "userStatus": 0
    }
])
def user_data(api_client, request):
    user = request.param
    response = api_client.post(f"{BASE_URL}/user", json=user)
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    yield user
    # Удаление пользователя после завершения теста
    response_delete = api_client.delete(f"{BASE_URL}/user/{user['username']}")
    assert response_delete.status_code == 200, f"Failed to delete user with username {user['username']}"


# Тест на создание пользователей с массивом
def test_create_users_with_array(api_client, user_data):
    url = f"{BASE_URL}/user/createWithArray"

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
    ("testuser1", "password123", 200),
    ("testuser2", "password123", 200),
    ("invaliduser", "wrongpassword", 400)
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

    if expected_status_code == 200:
        try:
            # Проверяем, что тело ответа содержит ожидаемое сообщение
            response_data = response.text.strip()
            print(f"User logged in successfully with username: {username}")

            # Проверяем наличие заголовков X-Expires-After и X-Rate-Limit
            assert 'X-Expires-After' in response.headers, "Missing 'X-Expires-After' header"
            assert 'X-Rate-Limit' in response.headers, "Missing 'X-Rate-Limit' header"
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
