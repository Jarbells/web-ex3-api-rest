from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Plataforma Comunidade API"
    API_V1_STR: str = "/api/v1"
    
    # auth0
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ALGORITHM: str
    AUTH0_ISSUER: str

    # database
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = ".env"
        extra = "ignore" # ignora variaveis extras no .env se tiver

# faltava esta linha para o import funcionar
settings = Settings()