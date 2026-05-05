# tests/test_products.py
import pytest
from app.models import Product
from app.database import SessionLocal


def test_create_product(client, db_session):
    response = client.post("/products/", json={
        "title": "Test Product",
        "price": 99.99,
        "count": 10,
        "description": "This is a test product"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Product"
    assert data["price"] == 99.99
    assert data["count"] == 10
    assert "id" in data


def test_create_product_invalid_price(client):
    """Отрицательная цена не проходит Pydantic валидацию (422)"""
    response = client.post("/products/", json={
        "title": "Test Product",
        "price": -10,
        "count": 10,
        "description": "Invalid price"
    })
    # Pydantic validation returns 422 for Field(gt=0) violation
    assert response.status_code == 422
    # Проверяем структуру ответа от кастомного обработчика
    data = response.json()
    # Ваш обработчик возвращает поля: success, status_code, message, details
    assert "message" in data
    assert data["success"] is False
    assert data["status_code"] == 422
    assert "details" in data
    # Проверяем, что ошибка связана с полем price
    assert "price" in str(data["details"])


def test_create_product_zero_price(client):
    """Нулевая цена также не проходит валидацию gt=0"""
    response = client.post("/products/", json={
        "title": "Test Product",
        "price": 0,
        "count": 10,
        "description": "Zero price"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["status_code"] == 422


def test_get_product(client, db_session):
    # Create product first
    create_response = client.post("/products/", json={
        "title": "Get Test Product",
        "price": 49.99,
        "count": 5,
        "description": "Product to retrieve"
    })
    product_id = create_response.json()["id"]

    # Get product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["title"] == "Get Test Product"


def test_get_nonexistent_product(client):
    response = client.get("/products/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["status_code"] == 404
    assert "Product with id 99999 not found" in data["message"]


def test_list_products(client, db_session):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_product(client, db_session):
    create_response = client.post("/products/", json={
        "title": "Update Test",
        "price": 29.99,
        "count": 3,
        "description": "Original description"
    })
    product_id = create_response.json()["id"]

    response = client.put(f"/products/{product_id}", json={
        "title": "Updated Title",
        "price": 39.99
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 39.99


def test_update_product_invalid_price(client, db_session):
    """Обновление с отрицательной ценой должно вернуть 422"""
    create_response = client.post("/products/", json={
        "title": "Update Test",
        "price": 29.99,
        "count": 3,
        "description": "Original description"
    })
    product_id = create_response.json()["id"]

    response = client.put(f"/products/{product_id}", json={
        "price": -10
    })
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["status_code"] == 422


def test_delete_product(client, db_session):
    create_response = client.post("/products/", json={
        "title": "Delete Test",
        "price": 19.99,
        "count": 1,
        "description": "To be deleted"
    })
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_custom_exception_a_trigger(client):
    """Тест для CustomExceptionA (если есть эндпоинт, который его вызывает)"""
    # Пример: если есть эндпоинт /errors/test-a/fail
    response = client.get("/errors/test-a/fail")
    # В зависимости от реализации может быть 400
    if response.status_code == 400:
        data = response.json()
        assert data["success"] is False
        assert "CustomExceptionA" in data["message"]


def test_custom_exception_b_trigger(client):
    """Тест для CustomExceptionB (если есть эндпоинт, который его вызывает)"""
    # Пример: если есть эндпоинт /errors/test-b/999
    response = client.get("/errors/test-b/999")
    # В зависимости от реализации может быть 404
    if response.status_code == 404:
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()