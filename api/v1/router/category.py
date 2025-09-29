from typing import List
from loguru import logger
import fastapi

from controller.category import CategoryController
from schemas.category import CategoryOut, CategoryIn, CategoryUpdate

category_router = fastapi.APIRouter(prefix="/categories")


@category_router.get("/", response_model=List[CategoryOut])
async def get_categories():
    logger.info("Router: Getting all categories")
    categories =  CategoryController.get_categories()
    return categories


@category_router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int):
    logger.info(f"Router: Getting Category with ID: {category_id}")
    return CategoryController.get_category_by_id(category_id)


@category_router.post("/", response_model=CategoryOut)
async def create_category(category: CategoryIn):
    return CategoryController.create_category(category)


@category_router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, category: CategoryUpdate):
    return CategoryController.update_category(category_id, category)


@category_router.delete("/{category_id}", response_model=CategoryOut)
async def delete_category(category_id: int):
    return CategoryController.delete_category(category_id)
