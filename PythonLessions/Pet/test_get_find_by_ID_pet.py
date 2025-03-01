import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тестовые данные: валидные и невалидные ID
test_data = [
    # Валидный ID
    (
        777,
        200
    ),
    # Невалидный ID (строка вместо числа)
    (
        "not_an_integer",
        400
    ),
    # Питомец не найден (ID не существует)
    (
        999999,
        404
    )
]

# Тест на поиск питомца по ID с параметризацией
@pytest.mark.parametrize("pet_id, expected_status_code", test_data)
def test_find_pet_by_id(api_client, pet_id, expected_status_code):
    url = f"{BASE_URL}/pet/{pet_id}"

    response = api_client.get(url)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        # Проверяем, что возвращенные данные содержат информацию о питомце
        response_data = response.json()
        assert response_data["id"] == pet_id, "Incorrect pet ID in response"
        print(f"Pet found successfully with ID: {response_data['id']}")
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
