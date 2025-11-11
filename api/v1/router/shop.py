from typing import List
from fastapi import Depends
from loguru import logger
import fastapi
from controller.shop import ShopController
from core.auth import get_current_user
from models import User
from schemas.shop import ShopOut, ShopIn, ShopUpdate

shop_router = fastapi.APIRouter(prefix="/shops")


@shop_router.get("/", response_model=List[ShopOut])
async def get_shops(current_user: User = Depends(get_current_user)):
    logger.info("Router: Getting all shops")
    return ShopController.get_shops()


@shop_router.get("/{shop_id}", response_model=ShopOut)
async def get_shop(shop_id: int,current_user: User = Depends(get_current_user)):
    logger.info(f"Router: Getting Shop with ID: {shop_id}")

    return ShopController.get_shop_by_id(shop_id)


@shop_router.post("/", response_model=ShopOut)
async def create_shop(shop: ShopIn,current_user: User = Depends(get_current_user)):
    return ShopController.create_shop(shop)


@shop_router.put("/{shop_id}", response_model=ShopOut)
async def update_shop(shop_id: int, shop: ShopUpdate,current_user: User = Depends(get_current_user)):
    return ShopController.update_shop(shop_id, shop)


@shop_router.delete("/{shop_id}")
async def delete_shop(shop_id: int,current_user: User = Depends(get_current_user)):
    return ShopController.delete_shop(shop_id)

