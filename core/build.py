from fastapi import FastAPI, responses

from core import setup as db_setup
from api.v1.router import user
from config.setting import app_settings


class AppBuilder:
    def __init__(self):
        self._app = FastAPI(title=app_settings.API_NAME,
                            description=app_settings.API_DESCRIPTION,
                            )

    def register_routes(self):
        """ Register all routes """

        self._app.include_router(
            user.user_router,
            prefix=app_settings.API_PREFIX,
            tags=["User"])

        @self._app.get("/", include_in_schema=False)
        def index():
            return responses.RedirectResponse(url="/docs")

    def register_database(self) -> None:
        db_setup.Base.metadata.create_all(bind=db_setup.database.get_engine())

    def get_app(self):
        self.register_routes()
        self.register_database()
        return self._app
