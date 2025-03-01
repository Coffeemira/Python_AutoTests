import pytest
import requests

from Pet.data_get import test_data, BASE_URL

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тест на добавление нового питомца с параметризацией
@pytest.mark.parametrize("pet_data, expected_status_code", test_data)
def test_add_new_pet(api_client, pet_data, expected_status_code):
    url = f"{BASE_URL}/pet"
    response = api_client.delete(url, json=pet_data)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        response_data = response.json()
        assert response_data["name"] == pet_data["name"], "Incorrect pet name in response"
        assert response_data["status"] == pet_data["status"], "Incorrect pet status in response"
        print(f"New pet added successfully with ID: {response_data['id']}")
    elif expected_status_code == 405:
        error_message = response.text
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")




