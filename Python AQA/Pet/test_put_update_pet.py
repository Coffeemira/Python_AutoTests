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


# Фикстура для создания и удаления ID питомца для теста на 404
@pytest.fixture
def deleted_pet_id(api_client, create_pet):
    pet_id = create_pet
    # Удаляем питомца
    response_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response_delete.status_code == 200 or response_delete.status_code == 404, f"Failed to delete pet with id {pet_id}"
    return pet_id


# Тестовые данные: валидные и невалидные
test_data = [
    # Валидный ID
    (0, "name", "available", 200),
    # Невалидный ID (строка вместо числа)
    ("not_an_integer", "InvalidID", "pending", 404),
    # Питомец не найден (ID не существует)
    (9223372036854775807, "NonExistentPet", "available", 404),
    # Некорректные символы в имени
    (0, "Special@Char", "pending", 200)  # Предполагаем, что сервер принимает такие символы
]


# Тест на обновление питомца с параметризацией
@pytest.mark.parametrize("pet_id, name, status, expected_status_code", test_data)
def test_update_pet_with_json_data(api_client, create_pet, pet_id, name, status, expected_status_code):
    # Используем ID созданного питомца для валидных тестов
    if pet_id == 0:
        pet_id = create_pet

    url = f"{BASE_URL}/pet"

    data = {
        "id": pet_id,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": name,
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": status
    }

    # Используем метод PUT для обновления питомца с данными в формате JSON
    response = api_client.put(url, json=data)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        try:
            # Проверяем, что возвращенные данные соответствуют отправленным
            response_data = response.json()
            assert "name" in response_data, f"Response JSON does not contain 'name' key: {response_data}"
            assert response_data[
                       "name"] == name, f"Incorrect pet name in response: expected {name}, got {response_data['name']}"
            assert "status" in response_data, f"Response JSON does not contain 'status' key: {response_data}"
            assert response_data[
                       "status"] == status, f"Incorrect pet status in response: expected {status}, got {response_data['status']}"
            print(f"Pet updated successfully with ID: {pet_id}")
        except KeyError as e:
            print(f"Response JSON does not have expected key: {e}")
            assert False, "Response JSON does not have expected key"
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
    elif expected_status_code in [400, 404]:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        try:
            error_message = response.json().get("message")
            assert error_message is not None, "Error message should be present in the response"
            print(f"Error message: {error_message}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
        except Exception as e:
            print(f"Unexpected error: {e}")
            assert False, "Unexpected error in response"


# Тест на неудачный запрос обновления питомца с 404 кодом
def test_update_pet_with_json_data_deleted_id(api_client, deleted_pet_id):
    url = f"{BASE_URL}/pet"

    data = {
        "id": deleted_pet_id,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "NonExistentPet",
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

    response = api_client.put(url, json=data)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} for ID {deleted_pet_id}"
    error_message = response.json().get("message")
    assert error_message is not None, "Error message should be present in the response"
    print(f"Error message: {error_message}")