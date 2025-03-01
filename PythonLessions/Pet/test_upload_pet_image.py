import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()

# Тестовые данные: ID питомца, дополнительные метаданные и путь к файлу изображения
test_data = [
    (
        1,  # petId
        "Test metadata",  # additionalMetadata
        "path/to/image.jpg"  # file path
    )
]


# Тест на загрузку изображения для питомца
@pytest.mark.parametrize("pet_id, additional_metadata, file_path", test_data)
def test_upload_pet_image(api_client, pet_id, additional_metadata, file_path):
    url = f"{BASE_URL}/pet/{pet_id}/uploadImage"

    # Открываем файл изображения для отправки
    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {'additionalMetadata': additional_metadata}

        response = api_client.post(url, files=files, data=data)

    # Проверяем статус-код ответа
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Проверяем содержимое ответа
    response_data = response.json()
    assert response_data["code"] == 200, "Incorrect code in response"
    assert response_data["type"] == "unknown", "Incorrect type in response"
    assert isinstance(response_data["message"], str), "Message should be a string"

    print(f"Image uploaded successfully for pet ID: {pet_id}")
