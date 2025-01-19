import pytest
from utils import logger


@pytest.mark.asyncio
async def test_create_speciality(async_client, token_admin):
    response = await async_client.post(
        "/api/v1/specialities",
        json={
            "name": "test_speciality1",
            "descriptions": "test_speciality1_description",
        },
        cookies={"access_token": token_admin[0]},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["speciality"]["name"] == "test_speciality1"
    assert data["speciality"]["descriptions"] == "test_speciality1_description"


@pytest.mark.asyncio
async def test_name_conflict_error_on_creation_speciality(async_client):
    response = await async_client.post(
        "/api/v1/specialities",
        json={
            "name": "test_speciality1",
            "descriptions": "test_speciality1_description",
        },
    )
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Speciality already exists"


@pytest.mark.asyncio
async def test_validate_error_on_creation_speciality(async_client):
    response = await async_client.post(
        "/api/v1/specialities",
        json={
            "name": "test_speciality2",
        },
    )
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][1] == "descriptions"
    assert data["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_get_speciality_by_id(async_client):
    response = await async_client.get(
        "/api/v1/specialities/3",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["speciality"]["name"] == "test_speciality1"
    assert data["speciality"]["descriptions"] == "test_speciality1_description"


@pytest.mark.asyncio
async def test_not_found_speciality(async_client):
    response = await async_client.get(
        "/api/v1/specialities/11",
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Speciality not found"


@pytest.mark.asyncio
async def test_update_speciality(async_client):
    response = await async_client.patch(
        "/api/v1/specialities/3",
        json={
            "name": "test_speciality22",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Speciality updated"
    assert data["speciality"]["name"] == "test_speciality22"
    assert data["speciality"]["descriptions"] == "test_speciality1_description"


@pytest.mark.asyncio
async def test_delete_speciality(async_client):
    response = await async_client.delete(
        "/api/v1/specialities/3",
    )
    assert response.status_code == 204
