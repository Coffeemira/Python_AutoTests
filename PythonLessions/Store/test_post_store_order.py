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
    assert response_delete.status_code == 200, f"Failed to delete pet with id {pet_id}"

# Тестовые данные для неудачных запросов получения питомца
test_data_failed = [
    ("test123", 400),
    ("3.14", 400),
    ("3,14", 400),
    ("№2", 400),
    (-500, 400),
    ("", 400),
    (0, 400),
]

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
                "id": 0,
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
        405
    )
]

# Тесты на неудачные запросы получения питомца
@pytest.mark.parametrize("pet_id, expected_status", test_data_failed)
def test_pet_get_failed(api_client, pet_id, expected_status):
    response = api_client.get(f"{BASE_URL}/pet/{pet_id}")
    assert response.status_code == expected_status

# Тест на неудачный запрос получения всех питомцев
def test_pet_get_failed2(api_client):
    response = api_client.get(f"{BASE_URL}/pet")
    assert response.status_code == 400

# Тест на успешный запрос получения питомца
def test_pet_get_success(api_client, create_pet):
    response = api_client.get(f"{BASE_URL}/pet/{create_pet}")
    assert response.status_code == 200

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
    elif expected_status_code == 405:
        error_message = response.text
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
