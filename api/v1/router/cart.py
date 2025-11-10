from typing import List

from fastapi import Depends
from loguru import logger
import fastapi

from core.auth import get_current_user
from models import User
from utils.session import SessionManager as DBSession

from controller.cart import CartController
from schemas.cart import CartOut, CartIn, CartUpdate
from schemas.cart_item import CartItemIn, CartItemOut

cart_router = fastapi.APIRouter(prefix="/carts")


@cart_router.get("/", response_model=List[CartOut])
async def get_carts(current_user: User = Depends(get_current_user)):
    logger.info("Router: Getting all carts")
    return CartController.get_carts()


@cart_router.get("/{cart_id}", response_model=CartOut)
async def get_cart(cart_id: int,current_user: User = Depends(get_current_user)):
    logger.info(f"Router: Getting Cart with ID: {cart_id}")
    return CartController.get_cart_by_id(cart_id)


@cart_router.post("/", response_model=CartOut)
async def create_cart(cart: CartIn,current_user: User = Depends(get_current_user)):
    with DBSession() as db:
        logger.info(f"Router: Creating Cart with: {cart}")
        cart_instance = CartController.create_cart(cart, db)
    return cart_instance.to_dict()

@cart_router.post("/add_to_cart", response_model=CartItemOut)
async def add_to_cart(cart_item_in: CartItemIn,current_user: User = Depends(get_current_user)):
    logger.info(f"Router: Adding Cart Item: {cart_item_in}")
    return CartController.add_to_cart(cart_item_in)

@cart_router.delete("/{cart_id}/remove_item/{cart_item_id}", response_model=CartOut)
async def remove_from_cart(cart_id:int, cart_item_id: int,current_user: User = Depends(get_current_user)):
    logger.info(f"Router: Deleting cart_item with ID: {cart_item_id} from cart with ID:: {cart_id}")
    return CartController.remove_from_cart(cart_id,cart_item_id)


@cart_router.put("/{cart_id}", response_model=CartOut)
async def update_cart(cart_id: int, cart: CartUpdate,current_user: User = Depends(get_current_user)):
    logger.info(f"Updating cart with ID: {cart_id} and payload:{cart}")
    return CartController.update_cart(cart_id, cart)


@cart_router.delete("/{cart_id}", response_model=CartOut)
async def delete_cart(cart_id: int,current_user: User = Depends(get_current_user)):
    logger.info(f"Router: Deleting cart with ID: {cart_id}")
    return CartController.delete_cart(cart_id)
