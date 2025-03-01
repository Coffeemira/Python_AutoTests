import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тестовые данные: валидные и невалидные
test_data = [
    # Валидные данные
    (
        777,
        "UpdatedName",
        "available",
        200
    ),
    # Невалидный ID (строка вместо числа)
    (
        "not_an_integer",
        "InvalidID",
        "pending",
        405
    ),
    # Недопустимый статус
    (
        777,
        "InvalidStatus",
        "invalid_status",
        405
    )
]

# Тест на обновление питомца с форм-данными с параметризацией
@pytest.mark.parametrize("pet_id, name, status, expected_status_code", test_data)
def test_update_pet_with_form_data(api_client, pet_id, name, status, expected_status_code):
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
            assert "name" in response_data, "Response does not contain 'name' key"
            assert "status" in response_data, "Response does not contain 'status' key"
            assert response_data["name"] == name, "Incorrect pet name in response"
            assert response_data["status"] == status, "Incorrect pet status in response"
            print(f"Pet updated successfully with ID: {pet_id}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"
    elif expected_status_code == 405:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        try:
            error_message = response.json().get("message")
            assert error_message is not None, "Error message should be present in the response"
            print(f"Error message: {error_message}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            assert False, "Response is not a valid JSON"

