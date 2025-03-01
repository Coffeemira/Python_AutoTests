import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания пользователя
@pytest.fixture
def create_user():
    response = requests.post(f'{BASE_URL}/user', json={
        "id": 0,
        "username": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "password": "string",
        "phone": "string",
        "userStatus": 0
    })
    data = response.json()
    pet_id = data['id']
    yield pet_id
    # Удаление питомца после завершения теста
    response_delete = requests.delete(f'{BASE_URL}/pet/{pet_id}')
    assert response_delete.status_code == 200, f"Failed to delete pet with id {pet_id}"

# Тестовые данные для неудачных запросов
test_data_failed = [
    ("test123", 404),
    ("3.14", 404),
    ("3,14", 404),
    ("№5", 404),
    (-500, 404),
    ("", 405),
    (0, 404),
]

# Тестовые данные для создания пользователя
invalid_user_data = [
    (
        {
            "id": "invalid_id",
            "username": "string",
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "phone": "string",
            "userStatus": 0
        },
        400
    ),
    (
        {
            "id": 0,
            "username": "",
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "phone": "string",
            "userStatus": 0
        },
        400
    ),
    (
        {
            "id": 0,
            "username": "string",
            "firstName": "",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "phone": "string",
            "userStatus": 0
        },
        400
    ),
    (
        {
            "id": 0,
            "username": "string",
            "firstName": "string",
            "lastName": "",
            "email": "string",
            "password": "string",
            "phone": "string",
            "userStatus": 0
        },
        400
    ),
    (
        {
            "id": 0,
            "username": "string",
            "firstName": "string",
            "lastName": "string",
            "email": "",
            "password": "string",
            "phone": "string",
            "userStatus": 0
        },
        400
    ),
]

# Тесты на неудачные запросы получения питомца
@pytest.mark.parametrize("pet_id, expected_status", test_data_failed)
def test_pet_get_failed(pet_id, expected_status):
    response = requests.get(f'{BASE_URL}/pet/{pet_id}')
    assert response.status_code == expected_status

# Тест на неудачный запрос получения всех питомцев
def test_pet_get_failed2():
    response = requests.get(f'{BASE_URL}/pet')
    assert response.status_code == 400

# Тест на успешный запрос получения питомца
def test_pet_get_success(create_pet):
    response = requests.get(f'{BASE_URL}/pet/{create_pet}')
    assert response.status_code == 200

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тест на создание пользователя с параметризацией
@pytest.mark.parametrize("user_data, expected_status_code", invalid_user_data)
def test_create_user(api_client, user_data, expected_status_code):
    url = f"{BASE_URL}/user"

    headers = {'Content-Type': 'application/json'}
    response = api_client.post(url, headers=headers, data=json.dumps(user_data))

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"