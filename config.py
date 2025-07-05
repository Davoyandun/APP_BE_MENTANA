from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application configuration
    app_name: str = "APP_BE_MENTANA"
    debug: bool = False
    version: str = "1.0.0"
    python_version: str = "3.11+"
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # AWS configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    aws_default_region: str = "us-east-1"
    
    # AWS Services
    aws_s3_bucket: Optional[str] = None
    aws_dynamodb_table: Optional[str] = None
    aws_sqs_queue_url: Optional[str] = None
    aws_sns_topic_arn: Optional[str] = None
    
    # AWS Local Development
    aws_endpoint_url: Optional[str] = None  # For DynamoDB local
    
    # Database (NoSQL - DynamoDB)
    # No traditional connection URL required
    
    # Redis (optional for cache)
    redis_url: Optional[str] = None
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()


def get_aws_config():
    """Returns AWS configuration"""
    config = {
        "region_name": settings.aws_region
    }
    
    # Add credentials if configured
    if settings.aws_access_key_id:
        config["aws_access_key_id"] = settings.aws_access_key_id
    if settings.aws_secret_access_key:
        config["aws_secret_access_key"] = settings.aws_secret_access_key
    
    # Add endpoint URL if configured (for local development)
    if settings.aws_endpoint_url:
        config["endpoint_url"] = settings.aws_endpoint_url
    
    return config


def get_dynamodb_table_name():
    """Returns DynamoDB table name"""
    return settings.aws_dynamodb_table


def get_redis_url():
    """Returns Redis URL (optional)"""
    return settings.redis_url 