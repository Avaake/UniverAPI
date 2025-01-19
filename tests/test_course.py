import pytest


@pytest.mark.asyncio
async def test_create_course(async_client, token_admin):
    response = await async_client.post(
        "/api/v1/courses",
        json={
            "name": "test_course1",
            "description": "test_course1",
            "credit_hours": 15,
            "user_id": 2,
        },
        cookies={"access_token": token_admin[0]},
    )

    data = response.json()
    assert response.status_code == 201
    assert "message" in data
    assert data["course"]["name"] == "test_course1"
    assert data["course"]["description"] == "test_course1"
    assert data["course"]["credit_hours"] == 15
    assert data["course"]["user_id"] == 2


@pytest.mark.asyncio
async def test_error_that_the_user_is_not_teacher(async_client):
    response = await async_client.post(
        "/api/v1/courses",
        json={
            "name": "test_course1",
            "description": "test_course1",
            "credit_hours": 15,
            "user_id": 3,
        },
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "User is not a teacher"


@pytest.mark.asyncio
async def test_user_not_found(async_client):
    response = await async_client.post(
        "/api/v1/courses",
        json={
            "name": "test_course1",
            "description": "test_course1",
            "credit_hours": 15,
            "user_id": 5,
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "User not found"


@pytest.mark.asyncio
async def test_name_conflict_error_on_creation_course(async_client):
    response = await async_client.post(
        "/api/v1/courses",
        json={
            "name": "test_course1",
            "description": "test_course1",
            "credit_hours": 15,
            "user_id": 2,
        },
    )
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Course already exists"


@pytest.mark.asyncio
async def test_validate_error_on_creation_course(async_client):
    response = await async_client.post(
        "/api/v1/courses",
        json={
            "name": "tes",
            "description": "test_course1",
        },
    )

    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "String should have at least 5 characters"

    assert data["detail"][2]["loc"][1] == "credit_hours"
    assert data["detail"][2]["msg"] == "Field required"

    assert data["detail"][3]["loc"][1] == "user_id"
    assert data["detail"][3]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_get_course_by_id(async_client):
    response = await async_client.get(
        "/api/v1/courses/2",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["course"]["name"] == "test_course1"
    assert data["course"]["description"] == "test_course1"


@pytest.mark.asyncio
async def test_update_course_by_id(async_client):
    response = await async_client.patch(
        "/api/v1/courses/2",
        json={
            "name": "test_course222",
            "credit_hours": 5,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["course"]["name"] == "test_course222"
    assert data["course"]["credit_hours"] == 5


@pytest.mark.asyncio
async def test_delete_course_by_id(async_client):
    response = await async_client.delete(
        "/api/v1/courses/2",
    )
    assert response.status_code == 204
