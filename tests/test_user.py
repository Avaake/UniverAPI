import pytest
from utils import delete_token, logger


@pytest.mark.asyncio
async def test_get_users_by_role(async_client):
    response = await async_client.get("/api/v1/users/roles/student")

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data["users"], list)


@pytest.mark.asyncio
async def test_update_user_role(
    token_admin,
    async_client,
):
    delete_token(async_client=async_client)
    response = await async_client.put(
        "/api/v1/users/3/role",
        json={"role_id": 2},
        cookies={"access_token": token_admin[0]},
    )

    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    assert data["user"]["role_id"] == 2


@pytest.mark.asyncio
async def test_me_profile(
    async_client,
    token_john_student,
):
    delete_token(async_client=async_client)

    response = await async_client.get(
        "/api/v1/users/me",
        cookies={"access_token": token_john_student[0]},
    )

    data = response.json()
    assert response.status_code == 200

    assert data["first_name"] == "john"
    assert data["last_name"] == "johnson"
    assert data["email"] == "john@gmail.com"
    assert data["phone_number"] == "+38077777777"


@pytest.mark.asyncio
async def test_update_user_by_id(async_client, token_john_student):
    delete_token(async_client=async_client)

    response = await async_client.patch(
        "/api/v1/users/3",
        json={
            "email": "testuser@gmail.con",
            "phone_number": "+38077777775",
        },
        cookies={"access_token": token_john_student[0]},
    )

    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    assert data["user"]["email"] == "testuser@gmail.con"
    assert data["user"]["phone_number"] == "+38077777775"


@pytest.mark.asyncio
async def test_delete_user(async_client, token_john_student):
    delete_token(async_client=async_client)

    response = await async_client.delete(
        "/api/v1/users/3",
        cookies={"access_token": token_john_student[0]},
    )

    assert response.status_code == 204
