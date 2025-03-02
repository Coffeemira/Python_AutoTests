import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Фикстура для создания питомца
@pytest.fixture
def create_pet(api_client):
    pet = {
        "id": 0,  # Убираем фиксированный ID, чтобы сервер сгенерировал уникальный ID
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
    response = api_client.post(f"{BASE_URL}/pet", json=pet)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"
    data = response.json()
    pet_id = data['id']
    yield pet_id, data  # Возвращаем ID и данные питомца
    # Удаление питомца после завершения теста
    response_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response_delete.status_code == 200 or response_delete.status_code == 404, f"Failed to delete pet with id {pet_id}"

# Тест на успешный запрос получения питомца
def test_pet_get_success(api_client, create_pet):
    pet_id, pet_data = create_pet
    response = api_client.get(f"{BASE_URL}/pet/{pet_id}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    response_data = response.json()
    assert response_data["name"] == pet_data["name"], "Incorrect pet name in response"
    assert response_data["status"] == pet_data["status"], "Incorrect pet status in response"
    print(f"Pet found successfully with ID: {response_data['id']}")

# Тест на добавление нового питомца
def test_add_new_pet(api_client):
    pet_data = {
        "id": 0,  # Убираем фиксированный ID, чтобы сервер сгенерировал уникальный ID
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "Charlie",
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
    url = f"{BASE_URL}/pet"
    response = api_client.post(url, json=pet_data)
    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    response_data = response.json()
    assert response_data["name"] == pet_data["name"], "Incorrect pet name in response"
    assert response_data["status"] == pet_data["status"], "Incorrect pet status in response"
    print(f"New pet added successfully with ID: {response_data['id']}")

# Фикстура для создания и удаления питомца
@pytest.fixture
def create_and_delete_pet(api_client, create_pet):
    pet_id, _ = create_pet
    response_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response_delete.status_code == 200, f"Failed to delete pet with id {pet_id}"
    return pet_id

# Тест на получение удаленного питомца для проверки кода 404
def test_get_deleted_pet(api_client, create_and_delete_pet):
    pet_id = create_and_delete_pet
    response = api_client.get(f"{BASE_URL}/pet/{pet_id}")
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