
from fastapi import FastAPI, responses

from core import setup as db_setup
from api.v1.router import product, user, shop, cart, category
from config.setting import app_settings


def register_database() -> None:
    db_setup.Base.metadata.create_all(bind=db_setup.database.get_engine())


class AppBuilder:
    def __init__(self):
        self._app = FastAPI(title=app_settings.API_NAME,
                            description=app_settings.API_DESCRIPTION,
                            )

    def register_routes(self):
        """ Register all routes """
        self._app.include_router(
            product.product_router,
            prefix=app_settings.API_PREFIX,
            tags=["Product"]
        )
        self._app.include_router(
            cart.cart_router,
            prefix=app_settings.API_PREFIX,
            tags=["Cart"]
        )

        self._app.include_router(
            category.category_router,
            prefix=app_settings.API_PREFIX,
            tags=["Category"]
        )
        self._app.include_router(
            user.user_router,
            prefix=app_settings.API_PREFIX,
            tags=["User"]
        )
        self._app.include_router(
            shop.shop_router,
            prefix=app_settings.API_PREFIX,
            tags=["Shop"]
        )

        @self._app.get("/", include_in_schema=False)
        def index():
            return responses.RedirectResponse(url="/docs")

    def get_app(self):
        self.register_routes()
        register_database()
        return self._app
