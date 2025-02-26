from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from models.category import Category
from schemas.category import CategoryIn, CategoryUpdate
from utils.session import SessionManager as DBSession
from fastapi.encoders import jsonable_encoder


class CategoryController:

    @staticmethod
    def get_categories():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all categories")
                categories = db.query(Category).all()
                categories_list = [category.to_dict() for category in categories]
                logger.info(f"Controller: Fetched Categories ==-> {categories_list}")
                return categories_list
        except Exception as e:
            logger.error(f"Controller: Error fetching categories: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching categories")

    @staticmethod
    def get_category_by_id(category_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching category with ID {category_id}")
                category = db.query(Category).filter(Category.id == category_id).first()
                if not category:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
                logger.info(f"Controller: Fetched Category ==-> {jsonable_encoder(category)}")
                return category.to_dict()
        except HTTPException as e:
            logger.error(f"Controller: Category with ID {category_id} not found")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error fetching category with ID {category_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching category")

    @staticmethod
    def create_category(category: CategoryIn):
        try:
            with DBSession() as db:
                category_instance = Category(**category.model_dump())
                logger.info(f"Controller: Creating category: {category_instance}")
                db.add(category_instance)
                db.commit()
                db.refresh(category_instance)
                logger.info(f"Controller: Category created with ID {category_instance.id}")
                return category_instance.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating category {category.username}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception as e:
            logger.error(f"Controller: Error creating category: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating category")

    @staticmethod
    def update_category(category_id: int, update_data: CategoryUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating category with ID {category_id}")
                category = db.query(Category).filter(Category.id == category_id).first()
                if not category:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(category, key, value)
                db.commit()
                db.refresh(category)
                logger.info(f"Controller: Category with ID {category_id} updated")
                return category.to_dict()

        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while updating category with ID {category_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception as e:
            logger.error(f"Controller: Error updating category with ID {category_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating category")

    @staticmethod
    def delete_category(category_id: int):
        with DBSession() as db:
            logger.info(f"Controller: Deleting category with ID {category_id}")
            category = db.query(Category).filter(Category.id == category_id).first()

            if not category:
                logger.error(f"Controller: Category with ID {category_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with ID {category_id} not found"
                )

            try:
                db.delete(category)
                db.commit()
                logger.info(f"Controller: Category with ID {category_id} deleted")
                return {"message": f"Category with ID {category_id} deleted successfully"}
            except SQLAlchemyError as e:
                db.rollback()  # Rollback transaction in case of error
                logger.error(f"Controller: SQLAlchemy Error while deleting category with ID {category_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error"
                )
            except Exception as e:
                db.rollback()
                logger.error(f"Controller: Unexpected error deleting category with ID {category_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error deleting category"
                )

