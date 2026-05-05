from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.routes import products, users, errors
from app.exceptions import setup_exception_handlers, ErrorResponse

app = FastAPI(
    title="FastAPI Demo Application",
    description="Application with migrations, custom exceptions, and validation",
    version="1.0.0"
)

setup_exception_handlers(app)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            details={"errors": exc.errors()}
        ).model_dump()
    )

@app.exception_handler(ValidationError)
async def pydantic_validation_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Pydantic validation error",
            details={"errors": exc.errors()}
        ).model_dump()
    )

app.include_router(products.router)
app.include_router(users.router)
app.include_router(errors.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to FastAPI Demo Application",
        "endpoints": {
            "products": "/products",
            "users": "/users",
            "error_testing": "/errors"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}