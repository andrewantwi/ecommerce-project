from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from models.product import Product
from schemas.product import ProductIn, ProductUpdate
from utils.session import SessionManager as DBSession
from fastapi.encoders import jsonable_encoder


class ProductController:

    @staticmethod
    def get_products():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all products")
                products = db.query(Product).all()
                products_list = [product.to_dict() for product in products]
                logger.info(f"Controller: Fetched Products ==-> {products_list}")
                return products_list
        except Exception as e:
            logger.error(f"Controller: Error fetching products: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching products")

    @staticmethod
    def get_product_by_id(product_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching product with ID {product_id}")
                product = db.query(Product).filter(Product.id == product_id).first()
                if not product:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
                logger.info(f"Controller: Fetched Product ==-> {jsonable_encoder(product)}")
                return product.to_dict()
        except HTTPException as e:
            logger.error(f"Controller: Product with ID {product_id} not found")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error fetching product with ID {product_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching product")

    @staticmethod
    def create_product(product: ProductIn):
        try:
            with DBSession() as db:
                product_instance = Product(**product.model_dump())
                logger.info(f"Controller: Creating product: {product_instance}")
                db.add(product_instance)
                db.commit()
                db.refresh(product_instance)
                logger.info(f"Controller: Product created with ID {product_instance.name}")
                return product_instance.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating product {product.name}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Controller: Error creating product: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating product: {str(e)}")

    @staticmethod
    def update_product(product_id: int, update_data: ProductUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating product with ID {product_id}")
                product = db.query(Product).filter(Product.id == product_id).first()
                if not product:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found")

                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(product, key, value)
                db.commit()
                db.refresh(product)
                logger.info(f"Controller: Product with ID {product_id} updated")
                return product.to_dict()

        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while updating product with ID {product_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
        except Exception as e:
            logger.error(f"Controller: Error updating product with ID {product_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating product: {str(e)}")

    @staticmethod
    def delete_product(product_id: int):
        with DBSession() as db:
            logger.info(f"Controller: Deleting product with ID {product_id}")
            product = db.query(Product).filter(Product.id == product_id).first()

            if not product:
                logger.error(f"Controller: Product with ID {product_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {product_id} not found"
                )

            try:
                db.delete(product)
                db.commit()
                logger.info(f"Controller: Product with ID {product_id} deleted")
                return {"message": f"Product with ID {product_id} deleted successfully"}
            except SQLAlchemyError as e:
                db.rollback()  # Rollback transaction in case of error
                logger.error(f"Controller: SQLAlchemy Error while deleting product with ID {product_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error:{str(e)}"
                )
            except Exception as e:
                db.rollback()
                logger.error(f"Controller: Unexpected error deleting product with ID {product_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error deleting product"
                )

