from pathlib import Path
from pydantic_settings import BaseSettings

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/lost_found"

    SECRET_KEY: str = "change-this-secret-key-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    USE_S3: bool = False
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = ""
    BASE_URL: str = "http://127.0.0.1:8000"

    MAX_UPLOAD_SIZE_MB: int = 5

    class Config:
        env_file = str(ENV_FILE)


settings = Settings()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
