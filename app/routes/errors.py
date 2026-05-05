from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional
from app.exceptions import CustomExceptionA, CustomExceptionB

router = APIRouter(prefix="/errors", tags=["error-testing"])

class UserData(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., gt=18, lt=120)
    email: EmailStr
    password: constr(min_length=8, max_length=16)  # type: ignore
    phone: Optional[str] = 'Unknown'

class ValidationErrorTestData(BaseModel):
    test_value: str

@router.get("/test-a/{value}")
def test_exception_a(value: str):
    """Endpoint that raises CustomExceptionA"""
    if value == "fail":
        raise CustomExceptionA("CustomExceptionA: Validation failed for test value")
    if value == "validate":
        raise CustomExceptionA("CustomExceptionA: Value requires validation")
    return {"message": f"Success! Value: {value}"}

@router.get("/test-b/{item_id}")
def test_exception_b(item_id: int):
    """Endpoint that raises CustomExceptionB"""
    if item_id > 100:
        raise CustomExceptionB(f"CustomExceptionB: Resource with id {item_id} not found")
    if item_id == 0:
        raise CustomExceptionB("CustomExceptionB: Invalid resource identifier")
    return {"message": f"Found resource with id {item_id}", "data": f"Resource-{item_id}"}

@router.post("/validate-user")
def validate_user_data(user: UserData):
    """Endpoint for validation testing"""
    if user.age < 18:
        raise CustomExceptionA(f"Age {user.age} is below minimum age of 18")
    if len(user.password) < 8:
        raise CustomExceptionA("Password must be at least 8 characters")
    return {
        "message": "User data is valid",
        "user": user.model_dump(exclude={"password"})
    }

@router.post("/validation-test")
def validation_test(data: ValidationErrorTestData):
    """Endpoint for custom validation error handling"""
    if not data.test_value:
        raise CustomExceptionA("Test value cannot be empty")
    if len(data.test_value) < 3:
        raise CustomExceptionA("Test value must be at least 3 characters")
    return {"message": f"Valid test value: {data.test_value}"}