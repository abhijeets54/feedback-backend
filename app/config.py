from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/feedback_db"

    # JWT
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Environment
    environment: str = "development"

    # CORS Origins
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.vercel.app",
        "https://*.railway.app",
        "https://*.render.com",
        "https://*.fly.dev",
    ]

    class Config:
        env_file = ".env"

    def get_cors_origins(self) -> List[str]:
        """Get CORS origins based on environment"""
        origins = self.allowed_origins.copy()

        # Add environment-specific origins
        if self.environment == "production":
            # Add your production frontend URL here
            frontend_url = os.getenv("FRONTEND_URL")
            if frontend_url:
                origins.append(frontend_url)

        return origins

settings = Settings()
