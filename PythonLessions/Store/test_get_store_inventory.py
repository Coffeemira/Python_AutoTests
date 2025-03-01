import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тест на получение инвентаря магазина
def test_get_store_inventory(api_client):
    url = f"{BASE_URL}/store/inventory"

    response = api_client.get(url)

    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Проверяем, что возвращенные данные являются словарем
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"

    # Проверяем, что возвращенные данные содержат ожидаемые ключи (статусы)
    expected_status_keys = ["available", "pending", "sold"]
    for key in expected_status_keys:
        assert key in response_data, f"Status '{key}' not found in inventory"
        assert isinstance(response_data[key], int), f"Value for status '{key}' should be an integer"

    print("Store inventory retrieved successfully")
