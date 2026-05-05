import pytest
from faker import Faker
from httpx import AsyncClient, ASGITransport
from app.main import app

fake = Faker()


@pytest.mark.asyncio
async def test_async_create_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        user_data = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=80),
            "email": fake.email(),
            "password": fake.password(length=10),
            "phone": fake.phone_number()
        }

        response = await client.post("/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "id" in data


@pytest.mark.asyncio
async def test_async_create_user_invalid_age():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        user_data = {
            "username": fake.user_name(),
            "age": 16,
            "email": fake.email(),
            "password": fake.password(length=10),
            "phone": fake.phone_number()
        }

        response = await client.post("/users/", json=user_data)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_async_get_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create user first
        create_data = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=80),
            "email": fake.email(),
            "password": fake.password(length=10),
            "phone": fake.phone_number()
        }
        create_response = await client.post("/users/", json=create_data)
        user_id = create_response.json()["id"]

        # Get user
        get_response = await client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["username"] == create_data["username"]


@pytest.mark.asyncio
async def test_async_get_nonexistent_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users/999999")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_async_delete_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create user
        create_data = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=80),
            "email": fake.email(),
            "password": fake.password(length=10),
            "phone": fake.phone_number()
        }
        create_response = await client.post("/users/", json=create_data)
        user_id = create_response.json()["id"]

        # Delete user
        delete_response = await client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204

        # Verify deleted
        get_response = await client.get(f"/users/{user_id}")
        assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_async_delete_twice():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create user
        create_data = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=80),
            "email": fake.email(),
            "password": fake.password(length=10),
            "phone": fake.phone_number()
        }
        create_response = await client.post("/users/", json=create_data)
        user_id = create_response.json()["id"]

        # Delete first time
        response1 = await client.delete(f"/users/{user_id}")
        assert response1.status_code == 204

        # Delete second time
        response2 = await client.delete(f"/users/{user_id}")
        assert response2.status_code == 404


@pytest.mark.asyncio
async def test_async_product_operations():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create product with faker
        product_data = {
            "title": fake.catch_phrase(),
            "price": fake.random_number(digits=3),
            "count": fake.random_int(min=0, max=100),
            "description": fake.text(max_nb_chars=200)
        }

        create_response = await client.post("/products/", json=product_data)
        assert create_response.status_code == 201
        product_id = create_response.json()["id"]

        # Get product
        get_response = await client.get(f"/products/{product_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == product_data["title"]

        # Update product
        update_data = {"price": 999.99}
        update_response = await client.put(f"/products/{product_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["price"] == 999.99

        # Delete product
        delete_response = await client.delete(f"/products/{product_id}")
        assert delete_response.status_code == 204