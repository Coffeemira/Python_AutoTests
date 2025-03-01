import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Фикстура для создания питомца
@pytest.fixture
def create_pet(api_client):
    response = api_client.post(f'{BASE_URL}/pet', json={
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
    })
    data = response.json()
    pet_id = data['id']
    yield pet_id
    # Удаление питомца после завершения теста
    response_delete = api_client.delete(f'{BASE_URL}/pet/{pet_id}')
    assert response_delete.status_code == 200, f"Failed to delete pet with id {pet_id}"

# Тестовые данные для неудачных запросов получения питомца
test_data_failed = [
    ("test123", 400),
    ("3.14", 400),
    ("3,14", 400),
    ("№1", 400),
    (-500, 400),
    ("", 400),
    (0, 400),
]

# Тест на неудачные запросы получения питомца с параметризацией
@pytest.mark.parametrize("pet_id, expected_status", test_data_failed)
def test_pet_get_failed(api_client, pet_id, expected_status):
    response = api_client.get(f'{BASE_URL}/pet/{pet_id}')
    assert response.status_code == expected_status

# Тест на успешный запрос получения питомца
def test_pet_get_success(create_pet, api_client):
    response = api_client.get(f'{BASE_URL}/pet/{create_pet}')
    assert response.status_code == 200

# Тестовые данные: валидные и невалидные
test_data_orders = [
    # Валидный ID
    (0, 200),
    # Невалидный ID (строка вместо числа)
    ("not_an_integer", 400),
    # Заказ не найден (ID не существует)
    (999999, 404),
]

# Тест на получение заказа по ID с параметризацией
@pytest.mark.parametrize("order_id, expected_status_code", test_data_orders)
def test_get_order_by_id(api_client, order_id, expected_status_code):
    url = f"{BASE_URL}/store/order/{order_id}"
    response = api_client.get(url)
    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
    if expected_status_code == 200:
        # Проверяем, что возвращенные данные соответствуют ожидаемым
        response_data = response.json()
        assert response_data["id"] == order_id, "Incorrect order ID in response"
        print(f"Order retrieved successfully with ID: {order_id}")
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