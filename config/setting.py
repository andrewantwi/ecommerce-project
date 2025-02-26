from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    API_NAME: str = "Ecommerce"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Ecommerce API"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433/ecommerce"

    class config:
        env_file = ".env"


app_settings = AppSettings()
