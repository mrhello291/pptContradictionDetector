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
    GEMINI_MODEL = "gemini-2.0-flash-exp"
    
    # Processing Configuration
    MAX_TOKENS = 8192
    TEMPERATURE = 0.1  # Low temperature for more consistent analysis
    
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