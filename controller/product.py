from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from models import Category, Shop
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

                product.view_count += 1
                db.commit()
                db.refresh(product)
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
                category = db.get(Category, product.category_id)
                shop = db.get(Shop, product.shop_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Category with id {product.category_id} does not exist. Please provide a valid category_id."
                    )
                if not shop:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"shop with id {product.shop_id} does not exist. Please provide a valid shop_id."
                    )

                product_instance = Product(**product.model_dump())
                logger.info(f"Controller: Creating product: {product_instance.to_dict()}")
                db.add(product_instance)
                db.commit()
                db.refresh(product_instance)
                logger.info(f"Controller: Product created with ID {product_instance.id}")
                return product_instance.to_dict()

        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating product {product.name}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred while creating the product."
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Controller: Error creating product: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while creating product."
            )

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
                db.rollback()
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

    @staticmethod
    def get_popular_products():
        with DBSession() as db:
            logger.info("Getting popular products")
            products = db.query(Product).order_by(Product.total_sales.desc()).limit(10).all()
            products_list = [product.to_dict() for product in products]
            logger.info(f"Popular products:: {products_list}")
        return products_list

    @staticmethod
    def get_trending_products():
        with DBSession() as db:
            logger.info("Getting Trending products")
            products = db.query(Product).order_by(Product.view_count.desc()).limit(10).all()
            products_list = [product.to_dict() for product in products]
            logger.info(f"Trending products:: {products_list}")
        return products_list

    @staticmethod
    def get_featured_products():
        with DBSession() as db:
            logger.info("Getting Featured products")
            products = db.query(Product).filter(Product.featured == True).limit(10).all()
            products_list = [product.to_dict() for product in products]
            logger.info(f"Featured products:: {products_list}")
        return products_list