from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    PROJECT_ID: str
    AUTH_URI: str
    TOKEN_URI: str
    AUTH_PROVIDER_X509_CERT_URL: str

    CLIENT_SECRET: str
    JAVASCRIPT_ORIGINS: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DB_URL: str

    RAWG_API_KEY: str

    IGDB_CLIENT_ID: str
    IGDB_CLIENT_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()
