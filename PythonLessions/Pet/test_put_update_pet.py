import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Фикстура для создания тестовых данных питомца
@pytest.fixture
def pet_test_data():
    return {
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

# Фикстура для создания питомца
@pytest.fixture
def create_pet(api_client, pet_test_data):
    response = api_client.post(f"{BASE_URL}/pet", json=pet_test_data)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"
    pet_id = response.json()['id']
    yield pet_id
    # Удаление питомца после завершения теста
    response_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response_delete.status_code == 200 or response_delete.status_code == 404, f"Failed to delete pet with id {pet_id}"

# Тестовые данные: валидные и невалидные
test_data = [
    (
        0,
        "name",
        "available",
        200
    ),
    (
        "not_an_integer",
        "InvalidID",
        "pending",
        400
    ),
    (
        9223372036854775807,  # Питомец с таким ID не существует
        "NonExistentPet",
        "available",
        404
    ),
    (
        0,
        "Special@Char",
        "pending",
        405
    )
]

# Тест на обновление питомца с параметризацией
@pytest.mark.parametrize("pet_id, name, status, expected_status_code", test_data)
def test_update_pet_with_form_data(api_client, create_pet, pet_id, name, status, expected_status_code):
    # Используем ID созданного питомца для валидных тестов
    if pet_id == 0:
        pet_id = create_pet

    url = f"{BASE_URL}/pet/{pet_id}"

    data = {
        "name": name,
        "status": status
    }

    response = api_client.post(url, data=data)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        try:
            # Проверяем, что возвращенные данные соответствуют отправленным
            response_data = response.json()
            assert "name" in response_data, f"Response JSON does not contain 'name' key: {response_data}"
            assert response_data["name"] == name, f"Incorrect pet name in response: expected {name}, got {response_data['name']}"
            assert "status" in response_data, f"Response JSON does not contain 'status' key: {response_data}"
            assert response_data["status"] == status, f"Incorrect pet status in response: expected {status}, got {response_data['status']}"
            print(f"Pet updated successfully with ID: {pet_id}")
        except KeyError as e:
            print(f"Response JSON does not have expected key: {e}")
            assert False, "Response JSON does not have expected key"
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
    elif expected_status_code in [400, 404, 405]:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        try:
            error_message = response.json().get("message")
            assert error_message is not None, "Error message should be present in the response"
            print(f"Error message: {error_message}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
