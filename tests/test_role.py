import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_create_role(async_client, token_admin):
    response = await async_client.post(
        "/api/v1/roles",
        json={"name": "test_role"},
        cookies={"access_token": token_admin[0]},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["role"]["name"] == "test_role"


@pytest.mark.asyncio
async def test_name_conflict_error_on_creation(
    async_client,
):
    response = await async_client.post(
        "/api/v1/roles",
        json={"name": "test_role"},
    )
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Role already exists"


@pytest.mark.asyncio
async def test_validate_error_on_creation(
    async_client,
):
    response = await async_client.post(
        "/api/v1/roles",
        json={"name": "te"},
    )
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "String should have at least 4 characters"


@pytest.mark.asyncio
async def test_get_roles(async_client):
    response = await async_client.get("/api/v1/roles")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data["roles"], list)
    assert data["roles"] is not None


@pytest.mark.asyncio
async def test_get_role(async_client):
    response = await async_client.get(
        "/api/v1/roles/5",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["role"]["name"] == "test_role"


@pytest.mark.asyncio
async def test_role_not_found(async_client):
    response = await async_client.get(
        "/api/v1/roles/10",
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Role not found"


@pytest.mark.asyncio
async def test_update_role(async_client):
    response = await async_client.put(
        "/api/v1/roles/5",
        json={"name": "test_role2"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Role updated"
    assert data["role"]["name"] == "test_role2"


@pytest.mark.asyncio
async def test_update_role_internal_error(async_client):
    with patch(
        "app.api.roles.dao.RoleDAO.update",
        side_effect=Exception("database error"),
    ):
        response = await async_client.put(
            "/api/v1/roles/5",
            json={"name": "test_role3"},
        )
        data = response.json()
        assert response.status_code == 500
        assert data["detail"] == "Failed to update user. Please try again later."


@pytest.mark.asyncio
async def test_delete_role(async_client):
    response = await async_client.delete(
        "/api/v1/roles/5",
    )
    assert response.status_code == 204
