import pytest


@pytest.mark.asyncio
async def test_hello_world(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"


@pytest.mark.asyncio
async def test_registration(async_client):
    # Дані для реєстрації користувача
    user_data = {
        "first_name": "testUser",
        "last_name": "testUser",
        "email": "testuser@gmail.com",
        "phone_number": "+380960220115",
        "password": "qwerty1",
        "confirm_password": "qwerty1",
    }

    # Надсилаємо POST запит для реєстрації
    response = await async_client.post("/api/v1/auth/register", json=user_data)

    # Перевіряємо статус код відповіді
    assert response.status_code == 201
