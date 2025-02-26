from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from models.cart_item import CartItem
from schemas.cart_item import CartItemIn, CartItemUpdate
from utils.session import SessionManager as DBSession


class CartItemController:

    @staticmethod
    def get_cart_items():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all cart_items")
                cart_items = db.query(CartItem).all()
                cart_items_list = [cart_item.to_dict() for cart_item in cart_items]
                return cart_items_list
        except Exception as e:
            logger.error(f"Controller: Error fetching cart_items: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching cart_items")

    @staticmethod
    def get_cart_item_by_id(cart_item_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching cart_item with ID: {cart_item_id}")
                cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
                if not cart_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CartItem not found")
                return cart_item.to_dict()
        except Exception as e:
            logger.error(f"Controller: Error fetching cart_item with ID {cart_item_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching cart_item")

    @staticmethod
    def create_cart_item(cart_item: CartItemIn):
        try:
            with DBSession() as db:
                cart_item_instance = CartItem(**cart_item.model_dump())
                db.add(cart_item_instance)
                db.commit()
                db.refresh(cart_item_instance)
                logger.info(f"Controller: CartItem created with ID {cart_item_instance.id}")
                return cart_item_instance.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating cart_item {cart_item.user_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @staticmethod
    def update_cart_item(cart_item_id: int, update_data: CartItemUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating cart_item with ID {cart_item_id}")
                cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
                if not cart_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CartItem not found")
                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(cart_item, key, value)
                db.commit()
                db.refresh(cart_item)
                return cart_item.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while updating cart_item with ID {cart_item_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @staticmethod
    def delete_cart_item(cart_item_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Deleting cart_item with ID {cart_item_id}")
                cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
                if not cart_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CartItem not found")
                db.delete(cart_item)
                db.commit()
                return {"message": "CartItem deleted successfully"}
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while deleting cart_item with ID {cart_item_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
