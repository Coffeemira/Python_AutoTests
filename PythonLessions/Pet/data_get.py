import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"

@pytest.fixture
def create_pet():
    response = requests.post(f'{BASE_URL}/pet', json={
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
    })

test_data = [
    # Валидные данные
    pytest.param(
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
        200,
    ),
    # Некорректные данные
    pytest.param(
        None,
        405,
    ),
    pytest.param(
        {
            "id": "abc",
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
        400,
    ),
]


