import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тестовые данные: валидные и невалидные
test_data = [
    # Валидные данные
    (
        {
            "id": 0,
            "petId": 0,
            "quantity": 0,
            "shipDate": "2025-03-01T09:40:47.994Z",
            "status": "placed",
            "complete": True
        },
        200
    ),
    # Невалидные данные (некорректный статус)
    (
        {
            "id": 0,
            "petId": 0,
            "quantity": 0,
            "shipDate": "2025-03-01T09:40:47.994Z",
            "status": "invalid_status",
            "complete": True
        },
        400
    )
]

# Тест на создание заказа с параметризацией
@pytest.mark.parametrize("order_data, expected_status_code", test_data)
def test_place_order(api_client, order_data, expected_status_code):
    url = f"{BASE_URL}/store/order"

    headers = {'Content-Type': 'application/json'}
    response = api_client.post(url, headers=headers, data=json.dumps(order_data))

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        # Проверяем, что возвращенные данные содержат ожидаемые поля
        response_data = response.json()
        assert "id" in response_data, "Response does not contain 'id' key"
        assert response_data["petId"] == order_data["petId"], "Incorrect pet ID in response"
        assert response_data["quantity"] == order_data["quantity"], "Incorrect quantity in response"
        assert response_data["status"] == order_data["status"], "Incorrect status in response"
        assert response_data["complete"] == order_data["complete"], "Incorrect complete status in response"
        print(f"Order placed successfully with ID: {response_data['id']}")
    elif expected_status_code == 400:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        error_message = response.json().get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
