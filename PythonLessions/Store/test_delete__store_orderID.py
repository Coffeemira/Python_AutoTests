import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тестовые данные: валидные и невалидные
test_data = [
    # Валидный ID
    (
        5,
        200
    ),
    # Невалидный ID (строка вместо числа)
    (
        "not_an_integer",
        400
    ),
    # Заказ не найден (ID не существует)
    (
        999999,
        404
    )
]

# Тест на удаление заказа по ID с параметризацией
@pytest.mark.parametrize("order_id, expected_status_code", test_data)
def test_delete_order(api_client, order_id, expected_status_code):
    url = f"{BASE_URL}/store/order/{order_id}"

    response = api_client.delete(url)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        print(f"Order deleted successfully with ID: {order_id}")
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

