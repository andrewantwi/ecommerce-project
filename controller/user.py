from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_

from core.auth import hash_password, generate_verification_token, send_verification_email
from models import Cart
from models.user import User
from controller.cart import CartController
from schemas.cart import CartIn
from schemas.user import UserIn, UserUpdate
from utils.session import SessionManager as DBSession
from fastapi.encoders import jsonable_encoder


class UserController:

    @staticmethod
    def get_users():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all users")
                users = db.query(User).all()
                users_list = [user.to_dict() for user in users]
                logger.info(f"Controller: Fetched Users ==-> {users_list}")
                return users_list
        except Exception as e:
            logger.error(f"Controller: Error fetching users: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching users")

    @staticmethod
    def get_user_by_id(user_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching user with ID {user_id}")
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                logger.info(f"Controller: Fetched User ==-> {jsonable_encoder(user)}")
                return user.to_dict()
        except HTTPException as e:
            logger.error(f"Controller: User with ID {user_id} not found")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error fetching user with ID {user_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching user")

    @staticmethod
    def create_user(user: UserIn):
        try:
            with DBSession() as db:
                exists = db.query(User).filter(
                    or_(User.full_name == user.full_name, User.email == user.email)
                ).first()

                if exists:
                    if exists.full_name == user.full_name:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this Full-name already exists"
                        )
                    if exists.email == user.email:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this Email already exists"
                        )

                user_instance = User(
                    full_name=user.full_name,
                    email=user.email,
                    hashed_password=hash_password(user.hashed_password),
                    is_active=False,
                    is_verified=False,
                    verification_token=generate_verification_token()
                )
                db.add(user_instance)
                db.commit()
                db.refresh(user_instance)

                cart_in = CartIn(user_id=user_instance.id)
                cart = CartController.create_cart(cart_in, db)
                user_instance.cart = cart

                db.commit()
                db.refresh(user_instance)


                send_verification_email(str(user.email), user.verification_token)

                return user_instance.to_dict()

        except HTTPException:
            raise

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this Email or Full-name already exists"
            )

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

    @staticmethod
    def update_user(user_id: int, update_data: UserUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating user with ID {user_id}")
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(user, key, value)
                db.commit()
                db.refresh(user)
                logger.info(f"Controller: User with ID {user_id} updated")
                return user.to_dict()

        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while updating user with ID {user_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Controller: Error updating user with ID {user_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error updating user: {str(e)}")

    @staticmethod
    def delete_user(user_id: int):
        with DBSession() as db:
            logger.info(f"Controller: Deleting user with ID {user_id}")
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                logger.error(f"Controller: User with ID {user_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id} not found"
                )

            try:
                db.delete(user)
                db.commit()
                logger.info(f"Controller: User with ID {user_id} deleted")
                return {"message": f"User with ID {user_id} deleted successfully"}
            except SQLAlchemyError as e:
                db.rollback()  # Rollback transaction in case of error
                logger.error(f"Controller: SQLAlchemy Error while deleting user with ID {user_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error:{str(e)}"
                )
            except Exception as e:
                db.rollback()
                logger.error(f"Controller: Unexpected error deleting user with ID {user_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error deleting user"
                )

    @staticmethod
    def get_user_cart(user_id: int):
        try:
            with DBSession() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    logger.warning(f"User with ID {user_id} not found.")
                    return {"message": "User not found"}, 404

                cart = db.query(Cart).filter(Cart.user_id == user_id).first()
                if not cart:
                    logger.info(f"No existing cart for user {user_id}. Creating a new one.")
                    cart = Cart(user_id=user_id)
                    db.add(cart)
                    db.commit()
                    db.refresh(cart)
                logger.info(f"Cart for user with ID:: {user_id}  cart:: {cart.to_dict()}")
                return cart.to_dict()
        except Exception as e:
            logger.error(f"Error fetching cart for user {user_id}: {e}")
            raise
