import pytest


@pytest.mark.asyncio
async def test_registration(async_client):
    user_data = {
        "first_name": "testUser",
        "last_name": "testUser",
        "email": "testuser@gmail.com",
        "phone_number": "+380960220115",
        "password": "qwerty1",
        "confirm_password": "qwerty1",
    }

    response = await async_client.post("/api/v1/auth/register", json=user_data)

    data = response.json()
    assert response.status_code == 201
    assert data["message"] == "You have been successfully registered!"


@pytest.mark.asyncio
async def test_login(async_client):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "qwerty1",
    }
    response = await async_client.post("/api/v1/auth/login", json=user_data)
    data = response.json()
    cookies = response.cookies

    assert response.status_code == 200
    assert data["message"] == "You have been logged in!"
    assert "access_token" in cookies
    assert "refresh_token" in cookies


@pytest.mark.asyncio
async def test_logout(async_client, token_admin):
    # async_client.cookies.set("access_token", token_admin[0])
    # async_client.cookies.set("refresh_token", token_admin[1])
    #
    cookies = {
        "access_token": token_admin[0],
        "refresh_token": token_admin[1],
    }
    response = await async_client.get("/api/v1/auth/logout", cookies=cookies)

    assert response.status_code == 200
    assert response.json()["message"] == "The user has successfully logged out"

    assert "access_token" not in async_client.cookies
    assert "refresh_token" not in async_client.cookies

    invalid_response = await async_client.get("/api/v1/auth/protected")
    assert invalid_response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_login(async_client, token_admin):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "qwerty_password",
    }
    response = await async_client.post("/api/v1/auth/login", json=user_data)

    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_refresh(async_client, token_admin):
    cookies = {
        "refresh_token": token_admin[1],
    }
    response = await async_client.get("/api/v1/auth/refresh", cookies=cookies)

    cookies_data = response.cookies
    assert response.status_code == 200
    assert "access_token" in cookies_data
    assert "refresh_token" in cookies_data
