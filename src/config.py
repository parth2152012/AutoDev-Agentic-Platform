"""Configuration Management"""
import os
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""
    DEBUG: bool = os.getenv('DEBUG', 'False') == 'True'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # API Configuration
    API_HOST: str = os.getenv('API_HOST', '0.0.0.0')
    API_PORT: int = int(os.getenv('API_PORT', '8000'))
    API_WORKERS: int = int(os.getenv('API_WORKERS', '4'))
    
    # Database Configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/autodev')
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    
    # ADO Configuration
    ADO_ORGANIZATION: str = os.getenv('ADO_ORGANIZATION', 'your-org')
    ADO_PROJECT: str = os.getenv('ADO_PROJECT', 'your-project')
    ADO_PAT_TOKEN: str = os.getenv('ADO_PAT_TOKEN', '')
    
    # LLM Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')
    
    # Agent Configuration
    MAX_WORKERS: int = int(os.getenv('MAX_WORKERS', '8'))
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '300'))
    
    @classmethod
    def from_env(cls):
        """Create config from environment variables"""
        return cls()

config = Config.from_env()
