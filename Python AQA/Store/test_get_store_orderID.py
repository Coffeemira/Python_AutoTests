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
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "string"}],
        "status": "available"
    })
    data = response.json()
    pet_id = data['id']
    yield pet_id
    # Удаление питомца после завершения теста
    response_delete = api_client.delete(f'{BASE_URL}/pet/{pet_id}')
    assert response_delete.status_code == 200, f"Failed to delete pet with id {pet_id}"

# Фикстура для удаленного питомца (для проверки 404 кода)
@pytest.fixture
def deleted_pet_id(api_client):
    # Создаем питомца без указания id (сервер сгенерирует уникальный)
    response = api_client.post(f'{BASE_URL}/pet', json={
        "category": {"id": 0, "name": "string"},
        "name": "deleted_doggie",
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "string"}],
        "status": "available"
    })
    data = response.json()
    pet_id = data['id']

    # Удаляем питомца
    response_delete = api_client.delete(f'{BASE_URL}/pet/{pet_id}')
    assert response_delete.status_code == 200, f"Failed to delete pet with id {pet_id}"

    return pet_id

# Тест на успешный запрос получения питомца
def test_pet_get_success(create_pet, api_client):
    response = api_client.get(f'{BASE_URL}/pet/{create_pet}')
    assert response.status_code == 200

# Тест на неудачный запрос получения питомца с 404 кодом
def test_pet_get_failed_404(api_client, deleted_pet_id):
    response = api_client.get(f'{BASE_URL}/pet/{deleted_pet_id}')
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} for ID {deleted_pet_id}"

# Тестовые данные: валидные и невалидные
test_data_orders = [
    (1, 200),
    ("not_an_integer", 404),  # Изменил ожидаемый статус-код на 404
    (999999, 404),
]

# Тест на получение заказа по ID с параметризацией
@pytest.mark.parametrize("order_id, expected_status_code", test_data_orders)
def test_get_order_by_id(api_client, order_id, expected_status_code):
    url = f"{BASE_URL}/store/order/{order_id}"
    response = api_client.get(url)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        response_data = response.json()
        assert response_data["id"] == order_id
        print(f"Order retrieved successfully with ID: {order_id}")
    else:
        error_message = response.json().get("message")
        assert error_message is not None
        print(f"Error message: {error_message}")