import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Фикстура для создания пользователя
@pytest.fixture
def create_user(api_client):
    user_data = {
        "id": 0,
        "username": "testuser",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 0
    }
    response = api_client.post(f'{BASE_URL}/user', json=user_data)
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    data = response.json()
    user_id = data.get('id')
    username = user_data["username"]
    yield username
    # Удаление пользователя после завершения теста
    response_delete = api_client.delete(f'{BASE_URL}/user/{username}')
    assert response_delete.status_code == 200, f"Failed to delete user with username {username}"

# Фикстура для создания питомца
@pytest.fixture
def create_pet(api_client):
    pet_data = {
        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    response = api_client.post(f'{BASE_URL}/pet', json=pet_data)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"
    data = response.json()
    pet_id = data['id']
    yield pet_id
    # Удаление питомца после завершения теста
    response_delete = api_client.delete(f'{BASE_URL}/pet/{pet_id}')
    assert response_delete.status_code == 200 or response_delete.status_code == 404, f"Failed to delete pet with id {pet_id}"

# Тестовые данные для неудачных запросов получения питомца
test_data_failed = [
    ("test123", 404),
    ("3.14", 404),
    ("3,14", 404),
    ("№5", 404),
    (-500, 404),
    ("", 404),
    (0, 404),
]

# Тест на неудачный запрос получения питомца с невалидным ID (строка вместо числа)
def test_pet_get_failed_not_an_integer(api_client):
    pet_id = "not_an_integer"
    url = f"{BASE_URL}/pet/{pet_id}"
    response = api_client.get(url)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    try:
        response_data = response.json()
        error_message = response_data.get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        assert False, "Response is not a valid JSON"
    except Exception as e:
        print(f"Unexpected error: {e}")
        assert False, "Unexpected error in response"

# Тест на неудачный запрос получения питомца с пустым ID
def test_pet_get_failed_empty_id(api_client):
    pet_id = ""
    url = f"{BASE_URL}/pet/{pet_id}"
    response = api_client.get(url)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    try:
        response_data = response.json()
        error_message = response_data.get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        assert False, "Response is not a valid JSON"
    except Exception as e:
        print(f"Unexpected error: {e}")
        assert False, "Unexpected error in response"

# Тест на неудачный запрос получения всех питомцев
def test_pet_get_failed2(api_client):
    url = f"{BASE_URL}/pet"
    response = api_client.get(url)
    assert response.status_code == 405, f"Expected status code 405, but got {response.status_code}"

# Тест на успешный запрос получения питомца
def test_pet_get_success(api_client, create_pet):
    url = f"{BASE_URL}/pet/{create_pet}"
    response = api_client.get(url)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    response_data = response.json()
    assert "name" in response_data, f"Response JSON does not contain 'name' key: {response_data}"
    assert response_data["name"] == "doggie", f"Incorrect pet name in response: expected 'doggie', got {response_data['name']}"
    print(f"Pet found successfully with ID: {response_data['id']}")

# Валидные данные для создания пользователя
valid_user_data = {
    "id": 0,
    "username": "testuser",
    "firstName": "Test",
    "lastName": "User",
    "email": "testuser@example.com",
    "password": "password123",
    "phone": "1234567890",
    "userStatus": 0
}

# Невалидные данные для создания пользователя (неверный тип данных для id)
invalid_user_data_1 = {
    "id": "invalid_id",
    "username": "string",
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "password": "string",
    "phone": "string",
    "userStatus": 0
}

# Невалидные данные для создания пользователя (пустое имя пользователя)
invalid_user_data_2 = {
    "id": 0,
    "username": "",
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "password": "string",
    "phone": "string",
    "userStatus": 0
}

# Тест на создание валидного пользователя
def test_create_valid_user(api_client):
    url = f"{BASE_URL}/user"
    headers = {'Content-Type': 'application/json'}
    response = api_client.post(url, headers=headers, json=valid_user_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    response_data = response.json()
    assert "code" in response_data, f"Response JSON does not contain 'code' key: {response_data}"
    assert response_data["code"] == 200, f"Incorrect code in response: expected 200, got {response_data['code']}"
    assert "type" in response_data, f"Response JSON does not contain 'type' key: {response_data}"
    assert response_data["type"] == "unknown", f"Incorrect type in response: expected 'unknown', got {response_data['type']}"
    assert "message" in response_data, f"Response JSON does not contain 'message' key: {response_data}"
    assert isinstance(response_data["message"], str), "Message should be a string"
    print(f"Valid user created successfully with ID: {response_data['message']}")

# Тест на создание пользователя с некорректными данными (неверный тип данных для id)
def test_create_user_invalid_id(api_client):
    url = f"{BASE_URL}/user"
    headers = {'Content-Type': 'application/json'}
    response = api_client.post(url, headers=headers, json=invalid_user_data_1)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    try:
        response_data = response.json()
        error_message = response_data.get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        assert False, "Response is not a valid JSON"
    except Exception as e:
        print(f"Unexpected error: {e}")
        assert False, "Unexpected error in response"

# Тест на создание пользователя с пустым именем пользователя
def test_create_user_empty_username(api_client):
    url = f"{BASE_URL}/user"
    headers = {'Content-Type': 'application/json'}
    response = api_client.post(url, headers=headers, json=invalid_user_data_2)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    try:
        response_data = response.json()
        error_message = response_data.get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        assert False, "Response is not a valid JSON"
    except Exception as e:
        print(f"Unexpected error: {e}")
        assert False, "Unexpected error in response"