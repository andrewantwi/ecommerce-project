from fastapi import FastAPI, responses

from core import setup as db_setup
from api.v1.router import doctor, appointment
from config.setting import app_settings
from api.v1.router import patient


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
            doctor.doctor_router,
            prefix=app_settings.API_PREFIX,
            tags=["Doctor"]
        )
        self._app.include_router(
            patient.patient_router,
            prefix=app_settings.API_PREFIX,
            tags=["Patient"]
        )

        self._app.include_router(
            appointment.appointment_router,
            prefix=app_settings.API_PREFIX,
            tags=["Appointment"]
        )

        @self._app.get("/", include_in_schema=False)
        def index():
            return responses.RedirectResponse(url="/docs")

    def get_app(self):
        self.register_routes()
        register_database()
        return self._app
