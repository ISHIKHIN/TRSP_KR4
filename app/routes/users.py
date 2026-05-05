from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, Dict
from itertools import count
from threading import Lock
from app.exceptions import CustomExceptionB

router = APIRouter(prefix="/users", tags=["users"])

# In-memory storage
db: Dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()


def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


# Pydantic models with validation
class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., gt=18, lt=120)
    email: EmailStr
    password: constr(min_length=8, max_length=16)  # type: ignore
    phone: Optional[str] = 'Unknown'


class UserOut(BaseModel):
    id: int
    username: str
    age: int
    email: str
    phone: Optional[str]


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    age: Optional[int] = Field(None, gt=18, lt=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn):
    # Check if email already exists
    for existing in db.values():
        if existing.get("email") == user.email:
            raise CustomExceptionB(f"User with email {user.email} already exists")

    user_id = next_user_id()
    user_data = user.model_dump()
    db[user_id] = user_data
    return {"id": user_id, **user_data}


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db:
        raise CustomExceptionB(f"User with id {user_id} not found")
    return {"id": user_id, **db[user_id]}


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in db:
        raise CustomExceptionB(f"User with id {user_id} not found")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        if value is not None:
            db[user_id][key] = value

    return {"id": user_id, **db[user_id]}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise CustomExceptionB(f"User with id {user_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)