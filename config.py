"""
Configuration module for PowerPoint Contradiction Detector.
"""
import os
from dotenv import load_dotenv
from typing import Optional, Tuple

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application."""
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    
    # Model Configuration
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    
    # Processing Configuration
    # Ensure correct types by converting from strings and providing defaults
    try:
        MAX_TOKENS: Optional[int] = int(os.getenv('MAX_TOKENS')) if os.getenv('MAX_TOKENS') is not None else None
    except (ValueError, TypeError):
        MAX_TOKENS = None

    try:
        TEMPERATURE: Optional[float] = float(os.getenv('TEMPERATURE')) if os.getenv('TEMPERATURE') is not None else None
    except (ValueError, TypeError):
        TEMPERATURE = None

    # Use sensible defaults if not provided or invalid
    if MAX_TOKENS is None:
        MAX_TOKENS = 2048  
    if TEMPERATURE is None:
        TEMPERATURE = 0.2
    
    # Image Configuration
    MAX_IMAGE_SIZE: Tuple[int, int] = (1024, 1024)
    IMAGE_QUALITY: int = 85
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Please set it in a .env file or environment variable."
            )
        return True