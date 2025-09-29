from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import User
from models.shop import Shop
from schemas.shop import ShopIn, ShopUpdate
from utils.session import SessionManager as DBSession
from fastapi.encoders import jsonable_encoder


class ShopController:

    @staticmethod
    def get_shops():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all shops")
                shops = db.query(Shop).all()
                shops_list = [shop.to_dict() for shop in shops]
                logger.info(f"Controller: Fetched Shops ==-> {shops_list}")
                return shops_list
        except Exception as e:
            logger.error(f"Controller: Error fetching shops: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching shops")

    @staticmethod
    def get_shop_by_id(shop_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching shop with ID {shop_id}")
                shop = db.query(Shop).filter(Shop.id == shop_id).first()
                if not shop:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
                logger.info(f"Controller: Fetched Shop ==-> {jsonable_encoder(shop)}")
                return shop.to_dict()
        except HTTPException as e:
            logger.error(f"Controller: Shop with ID {shop_id} not found")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error fetching shop with ID {shop_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching shop")

    @staticmethod
    def create_shop(shop: ShopIn):
        try:
            with DBSession() as db:
                owner = db.get(User,shop.owner_id)
                if not owner:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Shop with id {shop.owner_id} does not exist. Please provide a valid owner_id."
                    )

                shop_instance = Shop(**shop.model_dump())
                logger.info(f"Controller: Creating shop: {shop_instance.to_dict()}")
                db.add(shop_instance)
                db.commit()
                db.refresh(shop_instance)
                logger.info(f"Controller: Shop created with ID {shop_instance.name}")

                return shop_instance.to_dict()
        except IntegrityError as e:
            logger.error(f"Controller: Duplicate Shop name '{shop.name}': {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Shop with name '{shop.name}' already exists"
            )
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating shop {shop.name}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Controller: Error creating shop: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating shop: {str(e)}")

    from fastapi import HTTPException

    @staticmethod
    def update_shop(shop_id: int, update_data: ShopUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating shop with ID {shop_id}")
                shop = db.query(Shop).filter(Shop.id == shop_id).first()
                if not shop:
                    logger.info(f"Controller: Shop with ID {shop_id} not found")
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")

                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(shop, key, value)

                db.commit()
                db.refresh(shop)
                logger.info(f"Controller: Shop with ID {shop_id} updated")
                return shop.to_dict()

        except IntegrityError as e:
            db.rollback()
            logger.error(
                f"Controller: Duplicate Shop name '{update_data.name if update_data.name else 'N/A'}': {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Shop with name '{update_data.name}' already exists"
            )

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Controller: SQLAlchemy Error while updating shop with ID {shop_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

        except HTTPException:  # 👈 let FastAPI handle HTTPExceptions properly
            raise

        except Exception as e:
            logger.error(f"Controller: Error updating shop with ID {shop_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")

    @staticmethod
    def delete_shop(shop_id: int):
        with DBSession() as db:
            logger.info(f"Controller: Deleting shop with ID {shop_id}")
            shop = db.query(Shop).filter(Shop.id == shop_id).first()

            if not shop:
                logger.error(f"Controller: Shop with ID {shop_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Shop with ID {shop_id} not found"
                )

            try:
                db.delete(shop)
                db.commit()
                logger.info(f"Controller: Shop with ID {shop_id} deleted")
                return {"message": f"Shop with ID {shop_id} deleted successfully"}
            except SQLAlchemyError as e:
                db.rollback()  # Rollback transaction in case of error
                logger.error(f"Controller: SQLAlchemy Error while deleting shop with ID {shop_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error:{str(e)}"
                )
            except Exception as e:
                db.rollback()
                logger.error(f"Controller: Unexpected error deleting shop with ID {shop_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error deleting shop"
                )

