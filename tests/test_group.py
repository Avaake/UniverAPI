import pytest

@pytest.mark.asyncio
async def test_create_group(async_client, token_admin):
    response = await async_client.post(
        "/api/v1/groups",
        json={"name": "test_group"},
        cookies={"access_token": token_admin[0]},
    )

    data = response.json()
    assert response.status_code == 201
    assert "message" in data
    assert data["group"]["name"] == "TEST_GROUP"


@pytest.mark.asyncio
async def test_name_conflict_error_when_creating_group(async_client):
    response = await async_client.post(
        "/api/v1/groups",
        json={"name": "test_group"},
    )

    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Group already exists"


@pytest.mark.asyncio
async def test_validate_error_on_creation_group(async_client):
    response = await async_client.post(
        "/api/v1/groups",
        json={"name": "te"},
    )

    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "String should have at least 3 characters"


@pytest.mark.asyncio
async def test_get_group_by_id(async_client):
    response = await async_client.get(
        "/api/v1/groups/3",
    )

    data = response.json()
    assert response.status_code == 200
    assert data["group"]["name"] == "TEST_GROUP"
    assert data["group"]["id"] == 3


@pytest.mark.asyncio
async def test_role_not_found(async_client):
    response = await async_client.get(
        "/api/v1/groups/10",
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Group not found"


@pytest.mark.asyncio
async def test_update_group_by_id(async_client):
    response = await async_client.put(
        "/api/v1/groups/3",
        json={"name": "group2"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["group"]["name"] == "GROUP2"


@pytest.mark.asyncio
async def test_delete_group_by_id(async_client):
    response = await async_client.delete(
        "/api/v1/groups/3",
    )
    assert response.status_code == 204
