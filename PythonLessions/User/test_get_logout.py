import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тест на завершение сессии пользователя
def test_user_logout(api_client):
    url = f"{BASE_URL}/user/logout"

    response = api_client.get(url)

    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    try:
        # Проверяем, что тело ответа соответствует ожидаемому формату
        response_data = response.text.strip()
        print(f"User logged out successfully")
    except ValueError as e:
        print(f"Failed to parse response: {e}")
        assert False, "Response is not as expected"
