from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from models import CartItem, Product
from models.cart import Cart
from schemas.cart import CartIn, CartUpdate
from schemas.cart_item import CartItemOut, CartItemIn
from utils.session import SessionManager as DBSession


class CartController:

    @staticmethod
    def get_carts():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all carts")
                carts = db.query(Cart).all()
                carts_list = [cart.to_dict() for cart in carts]
                return carts_list
        except Exception as e:
            logger.error(f"Controller: Error fetching carts: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching carts")

    @staticmethod
    def get_cart_by_id(cart_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching cart with ID: {cart_id}")
                cart = db.query(Cart).filter(Cart.id == cart_id).first()
                if not cart:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
                return cart.to_dict()
        except Exception as e:
            logger.error(f"Controller: Error fetching cart with ID {cart_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching cart")


    @staticmethod
    def create_cart(cart: CartIn, db):
        try:
            cart_instance = Cart(**cart.model_dump())
            db.add(cart_instance)
            db.commit()
            db.refresh(cart_instance)
            logger.info(f"Controller: Cart created with ID {cart_instance.id}")
            return cart_instance
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating cart {cart.user_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"
            )
    @staticmethod
    def update_cart(cart_id: int, update_data: CartUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating cart with ID {cart_id}")
                cart = db.query(Cart).filter(Cart.id == cart_id).first()
                if not cart:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(cart, key, value)
                db.commit()
                db.refresh(cart)
                return cart.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while updating cart with ID {cart_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @staticmethod
    def delete_cart(cart_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Deleting cart with ID {cart_id}")
                cart = db.query(Cart).filter(Cart.id == cart_id).first()
                if not cart:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
                db.delete(cart)
                db.commit()
                return {"message": "Cart deleted successfully"}
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while deleting cart with ID {cart_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @staticmethod
    def add_to_cart(cart_item_in : CartItemIn):
        try:
            with DBSession() as db:

                cart = db.query(Cart).filter(Cart.user_id == cart_item_in.user_id).first()
                exists = db.query(Product).filter(Product.id == cart_item_in.product_id).first()
                if not exists:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

                if not cart:
                    cart = Cart(user_id=cart_item_in.user_id)
                    db.add(cart)
                    db.commit()
                    db.refresh(cart)

                cart_item = db.query(CartItem).filter(
                    CartItem.cart_id == cart.id,
                    CartItem.product_id == cart_item_in.product_id
                ).first()

                if cart_item:
                    # Update quantity and total price
                    cart_item.quantity += cart_item_in.quantity
                    cart_item.update_total_price()
                else:
                    # Create a new cart item
                    cart_item = CartItem(
                        cart_id=cart.id,
                        product_id=cart_item_in.product_id,
                        quantity=cart_item_in.quantity,
                        price=cart_item_in.price,
                        total_price=cart_item_in.quantity * cart_item_in.price
                    )
                    db.add(cart_item)

                # Recalculate total price
                cart.calculate_total()

                # Commit changes
                db.commit()
                db.refresh(cart)

                cart_item_instance = CartItemOut(**cart_item.to_dict())

                return cart_item_instance

        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy Error while adding item to cart: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"
            )
