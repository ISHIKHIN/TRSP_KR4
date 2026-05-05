from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict


class CustomExceptionA(Exception):

    def __init__(self, message: str = "Validation failed"):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST


class CustomExceptionB(Exception):

    def __init__(self, message: str = "Resource not found"):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND


class ProductNotFoundException(Exception):

    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with id {product_id} not found"
        self.status_code = status.HTTP_404_NOT_FOUND


class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    message: str
    details: Dict[str, Any] | None = None


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(CustomExceptionA)
    async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                status_code=exc.status_code,
                message=exc.message
            ).model_dump()
        )

    @app.exception_handler(CustomExceptionB)
    async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                status_code=exc.status_code,
                message=exc.message
            ).model_dump()
        )

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                status_code=exc.status_code,
                message=exc.message,
                details={"product_id": exc.product_id}
            ).model_dump()
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Invalid value provided",
                details={"error": str(exc)}
            ).model_dump()
        )