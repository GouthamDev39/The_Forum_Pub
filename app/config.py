from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_HOSTNAME : str
    DATABASE_USERNAME : str
    DATABASE_NAME : str
    DATABASE_PORT : str
    DATABASE_PASSWORD : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    class Config:
        env_file = ".env"

    #USe this for Docker

    # os.environ['DATABASE_HOSTNAME'] : str
    # os.environ['DATABASE_USERNAME'] : str
    # os.environ['DATABASE_NAME'] : str
    # os.environ['DATABASE_PORT'] : str
    # os.environ['DATABASE_PASSWORD'] : str
    # os.environ['SECRET_KEY'] : str
    # os.environ['ALGORITHM'] : str
    # os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] : int



settings = Settings()