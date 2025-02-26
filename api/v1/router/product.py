from typing import List
from loguru import logger
import fastapi

from controller.product import ProductController
from schemas.product import ProductOut, ProductIn, ProductUpdate

product_router = fastapi.APIRouter(prefix="/products")


@product_router.get("/", response_model=List[ProductOut])
async def get_products():
    logger.info("Router: Getting all products")
    products=  ProductController.get_products()
    return products


@product_router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int):
    logger.info(f"Router: Getting Product with ID: {product_id}")

    return ProductController.get_product_by_id(product_id)


@product_router.post("/", response_model=ProductOut)
async def create_product(product: ProductIn):
    return ProductController.create_product(product)


@product_router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product: ProductUpdate):
    return ProductController.update_product(product_id, product)


@product_router.delete("/{product_id}")
async def delete_product(product_id: int):
    return ProductController.delete_product(product_id)

