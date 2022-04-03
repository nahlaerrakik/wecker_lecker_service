from fastapi import FastAPI

from app.routes import category
from app.routes import menu
from app.routes import order
from app.routes import user

tags_metadata = [
    {"name": "Users", "description": "Manage Users"},
    {"name": "Categories", "description": "Manage Categories"},
    {"name": "Menus", "description": "Manage Menus"},
    {"name": "Orders", "description": "Manage Orders"},
]

api = FastAPI(openapi_tags=tags_metadata)

api.include_router(user.router)
api.include_router(category.router)
api.include_router(menu.router)
api.include_router(order.router)


@api.get("/")
def home():
    return "Wecker Lecker Service"
