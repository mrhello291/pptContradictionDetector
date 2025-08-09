"""
Configuration module for PowerPoint Contradiction Detector.
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application."""
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    
    # Model Configuration
    GEMINI_MODEL = os.getenv('GEMINI_MODEL')
    
    # Processing Configuration
    MAX_TOKENS = os.getenv('MAX_TOKENS')
    TEMPERATURE = os.getenv('TEMPERATURE')  # Low temperature for more consistent analysis
    
    # Image Configuration
    MAX_IMAGE_SIZE = (1024, 1024)
    IMAGE_QUALITY = 85
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Please set it in a .env file or environment variable."
            )
        return True 