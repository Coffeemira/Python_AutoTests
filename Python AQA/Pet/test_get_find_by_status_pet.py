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

# Тестовые данные: валидные и невалидные статусы
test_data = [
    # Валидные статусы
    (
        ["available", "pending", "sold"],
        200
    ),
    # Невалидный статус
    (
        ["invalid"],
        400
    ),
    # Не найденный питомец
    (
        [" -- "],
        404
    )
]

# Тест на поиск питомцев по статусу с параметризацией
@pytest.mark.parametrize("status_list, expected_status_code", test_data)
def test_find_pets_by_status(api_client, create_pet, status_list, expected_status_code):
    url = f"{BASE_URL}/pet/findByStatus"
    params = {"status": ",".join(status_list)}
    response = api_client.get(url, params=params)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        # Проверяем, что возвращенные данные содержат список питомцев
        response_data = response.json()
        assert isinstance(response_data, list), "Response should be a list of pets"
        for pet in response_data:
            assert pet["status"] in status_list, "Pet status does not match the requested status"
        print(f"Found {len(response_data)} pets with statuses: {status_list}")
    elif expected_status_code == 400:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        error_message = response.json().get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
    elif expected_status_code == 404:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        error_message = response.json().get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
