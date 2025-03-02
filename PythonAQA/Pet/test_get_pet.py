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
    response = api_client.post(f"{BASE_URL}/pet", json=pet)
    data = response.json()
    pet_id = data['id']
    yield pet_id
    # Удаление питомца после завершения теста
    response_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response_delete.status_code == 200 or response_delete.status_code == 404, f"Failed to delete pet with id {pet_id}"

# Фикстура для создания и удаления ID питомца
@pytest.fixture
def deleted_pet_id(api_client, create_pet):
    pet_id = create_pet
    # Удаляем питомца
    response_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response_delete.status_code == 200 or response_delete.status_code == 404, f"Failed to delete pet with id {pet_id}"
    return pet_id

# Тест на успешный запрос получения питомца
def test_pet_get_success(api_client, create_pet):
    response = api_client.get(f"{BASE_URL}/pet/{create_pet}")
    assert response.status_code == 200

# Тест на неудачный запрос получения питомца с 400 кодом
def test_pet_get_failed_400(api_client):
    invalid_pet_id = "invalid_id"
    response = api_client.get(f"{BASE_URL}/pet/{invalid_pet_id}")
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code} for ID {invalid_pet_id}"
    error_message = response.json().get("message")
    assert error_message is not None, "Error message should be present in the response"
    print(f"Error message: {error_message}")

# Тест на неудачный запрос получения питомца с 404 кодом
def test_pet_get_failed_404(api_client, deleted_pet_id):
    response = api_client.get(f"{BASE_URL}/pet/{deleted_pet_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} for ID {deleted_pet_id}"
    error_message = response.json().get("message")
    assert error_message is not None, "Error message should be present in the response"
    print(f"Error message: {error_message}")

# Тест на неудачный запрос получения всех питомцев
def test_pet_get_failed2(api_client):
    response = api_client.get(f"{BASE_URL}/pet")
    assert response.status_code == 405, f"Expected status code 405, but got {response.status_code}"

# Тестовые данные для создания питомца
pet_test_data = [
    # Валидные данные питомца
    (
        {
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
        },
        200
    ),
    # Невалидные данные питомца (например, отсутствует имя)
    (
        {
            "id": 0,
            "category": {
                "id": "none",
                "name": "string"
            },
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
        },
        400
    )
]

# Тест на добавление нового питомца с параметризацией
@pytest.mark.parametrize("pet_data, expected_status_code", pet_test_data)
def test_add_new_pet(api_client, pet_data, expected_status_code):
    url = f"{BASE_URL}/pet"
    response = api_client.post(url, json=pet_data)
    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
    if expected_status_code == 200:
        response_data = response.json()
        assert response_data["name"] == pet_data["name"], "Incorrect pet name in response"
        assert response_data["status"] == pet_data["status"], "Incorrect pet status in response"
        print(f"New pet added successfully with ID: {response_data['id']}")
    elif expected_status_code == 400:
        error_message = response.json().get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")