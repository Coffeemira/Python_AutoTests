import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Пример данных для создания пользователей
valid_users_data = [
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
]

# Тест на создание пользователей с массивом
def test_create_users_with_array(api_client):
    url = f"{BASE_URL}/user/createWithArray"

    headers = {'Content-Type': 'application/json'}
    response = api_client.post(url, headers=headers, data=json.dumps(valid_users_data))

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

if __name__ == "__main__":
    pytest.main([__file__])