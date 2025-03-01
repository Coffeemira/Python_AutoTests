from Pet.data_get import test_data, BASE_URL
import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"


# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()


# Тест на обновление питомца с параметризацией
@pytest.mark.parametrize("pet_data, expected_status_code", test_data)
def test_update_pet(api_client, pet_data, expected_status_code):
    url = f"{BASE_URL}/pet"

    response = api_client.put(url, json=pet_data)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        # Проверяем, что возвращенные данные соответствуют отправленным
        response_data = response.json()
        assert response_data["name"] == pet_data["name"], "Incorrect pet name in response"
        assert response_data["status"] == pet_data["status"], "Incorrect pet status in response"
        print(f"Pet updated successfully with ID: {response_data['id']}")
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
    elif expected_status_code == 405:
        # Проверяем, что тело ответа содержит сообщение об ошибке
        error_message = response.json().get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")

