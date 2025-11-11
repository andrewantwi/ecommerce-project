from fastapi import Depends
from loguru import logger
import fastapi
from controller.product import ProductController
from core.auth import get_current_user
from models import User
from schemas.product import HomepageProductsResponse

homepage_router = fastapi.APIRouter(prefix="/homepage")


@homepage_router.get("/", response_model=HomepageProductsResponse)
def get_homepage_products(current_user: User = Depends(get_current_user)):
    logger.info("Router: Fetching products for the Homepage")
    popular = ProductController.get_popular_products()
    trending = ProductController.get_trending_products()
    featured = ProductController.get_featured_products()

    homepage_products = {
        "popular": popular,
        "trending": trending,
        "featured": featured,
    }
    logger.info(f"Router: Fetched Products :: {homepage_products}")

    return homepage_products