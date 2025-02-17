from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
from fastapi.openapi.utils import get_openapi
from app.books.routers import books as books_router
from app.users.routers import user as user_router
from app.orders.routers import orders as orders_router

app = FastAPI()
app.include_router(user_router)
app.include_router(books_router)
app.include_router(orders_router)

app.add_middleware(SessionMiddleware, secret_key="fastapi_project")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI",
        version="1.0.0",
        description="This is an API with Bearer authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path:
            path[method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
