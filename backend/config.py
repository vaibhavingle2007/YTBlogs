"""
Configuration settings for the YouTube to Blog Converter API
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Find the project root directory (where .env should be)
current_dir = Path(__file__).parent  # backend directory
project_root = current_dir.parent    # project root directory

# Load environment variables from project root
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

print(f"🔧 Config: Looking for .env at: {env_path}")
print(f"🔧 Config: .env exists: {env_path.exists()}")

class Settings:
    """Application settings"""
    
    # Server configuration
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # API Keys
    YOUTUBE_API_KEY: Optional[str] = os.getenv("YOUTUBE_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    NEBIUS_API_KEY: Optional[str] = os.getenv("NEBIUS_API_KEY")
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]  # In production, specify your frontend domain
    
    # Application metadata
    APP_NAME: str = "YouTube to Blog Converter API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Convert YouTube videos into well-structured blog posts"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.DEBUG
    
    @property
    def has_youtube_api(self) -> bool:
        """Check if YouTube API key is configured"""
        return self.YOUTUBE_API_KEY is not None and len(self.YOUTUBE_API_KEY.strip()) > 0
    
    @property
    def has_openai_api(self) -> bool:
        """Check if OpenAI API key is configured"""
        return self.OPENAI_API_KEY is not None and len(self.OPENAI_API_KEY.strip()) > 0

    @property
    def has_nebius_api(self) -> bool:
        """Check if Nebius API key is configured"""
        return self.NEBIUS_API_KEY is not None and len(self.NEBIUS_API_KEY.strip()) > 0

# Global settings instance
settings = Settings() 