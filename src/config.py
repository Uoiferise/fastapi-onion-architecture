import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))


class Settings:
    MODE: str = os.environ.get('MODE')

    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: int = os.environ.get('DB_PORT')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASS: str = os.environ.get('DB_PASS')
    DB_NAME: str = os.environ.get('DB_NAME')

    DB_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


settings = Settings()
