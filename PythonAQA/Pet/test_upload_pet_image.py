import pytest
import requests
import json
import os
from tempfile import NamedTemporaryFile

BASE_URL = "https://petstore.swagger.io/v2"


# Фикстура для создания клиента API
@pytest.fixture
def api_client():
    return requests.Session()


# Фикстура для создания питомца
@pytest.fixture
def create_pet(api_client):
    pet = {
        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    response = api_client.post(f"{BASE_URL}/pet", json=pet)
    assert response.status_code == 200, f"Failed to create pet: {response.text}"
    data = response.json()
    pet_id = data['id']
    yield pet_id
    # Удаление питомца после завершения теста
    response_delete = api_client.delete(f"{BASE_URL}/pet/{pet_id}")
    assert response_delete.status_code == 200, f"Failed to delete pet with id {pet_id}"


# Тестовые данные для загрузки изображения питомца
test_data = [
    (
        1,  # petId (будет заменен на ID созданного питомца)
        "Test metadata",  # additionalMetadata
        "image.jpg"  # file path (будет создан временный файл)
    )
]

# Тестовые данные для создания питомца
pet_test_data = [
    # Валидные данные питомца
    (
        {
            "id": 0,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": "doggie",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "available"
        },
        200
    ),
    # Невалидные данные питомца (например, отсутствует имя)
    (
        {
            "id": 0,
            "category": {
                "id": "none",
                "name": "string"
            },
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "available"
        },
        400
    )
]


# Тест на загрузку изображения для питомца
@pytest.mark.parametrize("pet_id, additional_metadata, file_path", test_data)
def test_upload_pet_image(api_client, create_pet, pet_id, additional_metadata, file_path):
    # Используем ID созданного питомца для валидных тестов
    if pet_id == 1:
        pet_id = create_pet

    url = f"{BASE_URL}/pet/{pet_id}/uploadImage"

    # Создаем временный файл изображения
    with NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc`\x18\xe7`\xe0\x00\x00\x00\x02\x00\x01\xe2!\x9b\x00\x00\x00\x00IEND\xaeB`\x82')
        temp_file.flush()
        file_path = temp_file.name

    try:
        # Открываем временный файл изображения для отправки
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
    finally:
        # Удаляем временный файл
        os.remove(file_path)


# Тест на добавление нового питомца с параметризацией
@pytest.mark.parametrize("pet_data, expected_status_code", pet_test_data)
def test_add_new_pet(api_client, pet_data, expected_status_code):
    url = f"{BASE_URL}/pet"
    response = api_client.post(url, json=pet_data)

    # Проверяем статус-код ответа
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    if expected_status_code == 200:
        response_data = response.json()
        assert response_data["name"] == pet_data["name"], "Incorrect pet name in response"
        assert response_data["status"] == pet_data["status"], "Incorrect pet status in response"
        print(f"New pet added successfully with ID: {response_data['id']}")
    elif expected_status_code == 400:
        error_message = response.json().get("message")
        assert error_message is not None, "Error message should be present in the response"
        print(f"Error message: {error_message}")