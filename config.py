from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER", "default_user")
DB_PASS = os.getenv("DB_PASS", "default_password")
DB_NAME = os.getenv("DB_NAME", "default_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)

REAL_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

FIXER_API_URL = os.getenv("FIXER_API_URL", "default_api_url")
API_KEY = os.getenv("API_KEY", "default_api_key")


