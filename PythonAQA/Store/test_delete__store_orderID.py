import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Фикстура для создания заказа
@pytest.fixture
def create_order(api_client):
    order_data = {
        "id": 0,
        "petId": 0,
        "quantity": 0,
        "shipDate": "2023-10-01T00:00:00.000Z",
        "status": "placed",
        "complete": False
    }
    response = api_client.post(f'{BASE_URL}/store/order', json=order_data)
    assert response.status_code == 200, f"Failed to create order: {response.text}"
    data = response.json()
    order_id = data['id']
    print(f"Created order with ID: {order_id}")  # Логирование ID созданного заказа
    yield order_id
    # Удаление заказа после завершения теста
    response_delete = api_client.delete(f'{BASE_URL}/store/order/{order_id}')
    assert response_delete.status_code == 200 or response_delete.status_code == 404, f"Failed to delete order with id {order_id}"

# Тестовые данные: валидные и невалидные
test_data_delete_order = [
    # Валидный ID
    ("create_order", 200),
    # Невалидный ID (строка вместо числа)
    ("not_an_integer", 404),  # Ожидаем 404 вместо 400
    # Заказ не найден (ID не существует)
    (999999, 404),
]

# Тест на удаление заказа по ID с параметризацией
@pytest.mark.parametrize("order_id, expected_status_code", test_data_delete_order)
def test_delete_order(api_client, order_id, expected_status_code, create_order):
    if order_id == "create_order":
        order_id = create_order
    url = f"{BASE_URL}/store/order/{order_id}"
    response = api_client.delete(url)
    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
    if expected_status_code == 200:
        try:
            # Проверяем, что тело ответа соответствует отправленным данным
            response_data = response.json()
            assert "code" in response_data, f"Response JSON does not contain 'code' key: {response_data}"
            assert response_data["code"] == 200, f"Incorrect code in response: expected 200, got {response_data['code']}"
            assert "type" in response_data, f"Response JSON does not contain 'type' key: {response_data}"
            assert response_data["type"] == "unknown", f"Incorrect type in response: expected 'unknown', got {response_data['type']}"
            assert "message" in response_data, f"Response JSON does not contain 'message' key: {response_data}"
            assert isinstance(response_data["message"], str), "Message should be a string"
            print(f"Order deleted successfully with ID: {order_id}")
        except KeyError as e:
            print(f"Response JSON does not have expected key: {e}")
            assert False, "Response JSON does not have expected key"
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
        except Exception as e:
            print(f"Unexpected error: {e}")
            assert False, "Unexpected error in response"
    elif expected_status_code in [400, 404]:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        try:
            response_data = response.json()
            error_message = response_data.get("message")
            assert error_message is not None, "Error message should be present in the response"
            print(f"Error message: {error_message}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
        except Exception as e:
            print(f"Unexpected error: {e}")
            assert False, "Unexpected error in response"

# Фикстура для создания заказа без удаления после теста
@pytest.fixture
def order_without_deletion(api_client):
    order_data = {
        "id": 0,
        "petId": 0,
        "quantity": 0,
        "shipDate": "2023-10-01T00:00:00.000Z",
        "status": "placed",
        "complete": False
    }
    response = api_client.post(f'{BASE_URL}/store/order', json=order_data)
    assert response.status_code == 200, f"Failed to create order: {response.text}"
    data = response.json()
    order_id = data['id']
    print(f"Created order with ID: {order_id}")  # Логирование ID созданного заказа
    yield order_id
    # Не удаляем заказ после завершения теста

# Тест на удаление заказа по ID с параметризацией, используя заказ без удаления
@pytest.mark.parametrize("order_id, expected_status_code", test_data_delete_order)
def test_delete_order_no_cleanup(api_client, order_id, expected_status_code, order_without_deletion):
    if order_id == "create_order":
        order_id = order_without_deletion
    url = f"{BASE_URL}/store/order/{order_id}"
    response = api_client.delete(url)
    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
    if expected_status_code == 200:
        try:
            # Проверяем, что тело ответа соответствует отправленным данным
            response_data = response.json()
            assert "code" in response_data, f"Response JSON does not contain 'code' key: {response_data}"
            assert response_data["code"] == 200, f"Incorrect code in response: expected 200, got {response_data['code']}"
            assert "type" in response_data, f"Response JSON does not contain 'type' key: {response_data}"
            assert response_data["type"] == "unknown", f"Incorrect type in response: expected 'unknown', got {response_data['type']}"
            assert "message" in response_data, f"Response JSON does not contain 'message' key: {response_data}"
            assert isinstance(response_data["message"], str), "Message should be a string"
            print(f"Order deleted successfully with ID: {order_id}")
        except KeyError as e:
            print(f"Response JSON does not have expected key: {e}")
            assert False, "Response JSON does not have expected key"
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
        except Exception as e:
            print(f"Unexpected error: {e}")
            assert False, "Unexpected error in response"
    elif expected_status_code in [400, 404]:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        try:
            response_data = response.json()
            error_message = response_data.get("message")
            assert error_message is not None, "Error message should be present in the response"
            print(f"Error message: {error_message}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
        except Exception as e:
            print(f"Unexpected error: {e}")
            assert False, "Unexpected error in response"

# Тест на неудачный запрос удаления заказа с 404 кодом, используя заказ без удаления
def test_delete_order_failed_404_no_cleanup(api_client, order_without_deletion):
    response = api_client.delete(f'{BASE_URL}/store/order/{order_without_deletion}')
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} for ID {order_without_deletion}"
    response_data = response.json()
    assert "code" in response_data, f"Response JSON does not contain 'code' key: {response_data}"
    assert response_data["code"] == 200, f"Incorrect code in response: expected 200, got {response_data['code']}"
    assert "type" in response_data, f"Response JSON does not contain 'type' key: {response_data}"
    assert response_data["type"] == "unknown", f"Incorrect type in response: expected 'unknown', got {response_data['type']}"
    assert "message" in response_data, f"Response JSON does not contain 'message' key: {response_data}"
    assert isinstance(response_data["message"], str), "Message should be a string"
    print(f"Order deleted successfully with ID: {order_without_deletion}")
    # Повторная попытка удаления заказа, который уже удален
    response = api_client.delete(f'{BASE_URL}/store/order/{order_without_deletion}')
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} for ID {order_without_deletion}"
    # Проверяем, что тело ответа содержит сообщение об ошибке
    try:
        response_data = response.json()
        error_message = response_data.get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        assert False, "Response is not a valid JSON"
    except Exception as e:
        print(f"Unexpected error: {e}")
        assert False, "Unexpected error in response"