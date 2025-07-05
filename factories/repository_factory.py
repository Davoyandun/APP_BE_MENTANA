"""
Repository Factory for APP_BE_MENTANA

This factory centralizes the creation of repository instances,
making it easier to manage dependencies and switch implementations.
"""

from typing import Optional
from domain.src.repositories.user_repository import UserRepository
from adapters.repositories.aws_dynamodb_user_repository import AWSDynamoDBUserRepository
from config import settings
import structlog

logger = structlog.get_logger()


class RepositoryFactory:
    """
    Factory for creating repository instances.
    
    This factory follows the Factory pattern to centralize repository creation
    and make it easier to switch between different implementations.
    """
    
    _user_repository_instance: Optional[UserRepository] = None
    
    @classmethod
    def create_user_repository(cls) -> UserRepository:
        """
        Creates and returns a user repository instance.
        
        Returns:
            UserRepository: Configured user repository instance
            
        Raises:
            ValueError: If repository configuration is invalid
        """
        if cls._user_repository_instance is None:
            logger.info("Creating new user repository instance")
            
            # Validate configuration
            if not settings.aws_dynamodb_table:
                raise ValueError("AWS DynamoDB table name not configured")
            
            # Create repository instance
            cls._user_repository_instance = AWSDynamoDBUserRepository(
                table_name=settings.aws_dynamodb_table
            )
            
            logger.info("User repository instance created", 
                       table_name=settings.aws_dynamodb_table)
        
        return cls._user_repository_instance
    
    @classmethod
    def get_user_repository(cls) -> UserRepository:
        """
        Gets the existing user repository instance or creates a new one.
        
        Returns:
            UserRepository: User repository instance
        """
        return cls.create_user_repository()
    
    @classmethod
    def reset_user_repository(cls):
        """
        Resets the user repository instance (useful for testing).
        """
        cls._user_repository_instance = None
        logger.info("User repository instance reset")
    
    @classmethod
    def create_repository_by_type(cls, repository_type: str, **kwargs) -> UserRepository:
        """
        Creates a repository instance based on the specified type.
        
        Args:
            repository_type: Type of repository to create
            **kwargs: Additional configuration parameters
            
        Returns:
            UserRepository: Repository instance
            
        Raises:
            ValueError: If repository type is not supported
        """
        if repository_type.lower() == "dynamodb":
            table_name = kwargs.get("table_name", settings.aws_dynamodb_table)
            if not table_name:
                raise ValueError("Table name is required for DynamoDB repository")
            
            return AWSDynamoDBUserRepository(table_name=table_name)
        
        elif repository_type.lower() == "memory":
            # For future implementation of in-memory repository
            # from adapters.repositories.memory_user_repository import MemoryUserRepository
            # return MemoryUserRepository()
            raise ValueError("Memory repository not yet implemented")
        
        else:
            raise ValueError(f"Unsupported repository type: {repository_type}")
    
    @classmethod
    def get_repository_config(cls) -> dict:
        """
        Returns the current repository configuration.
        
        Returns:
            dict: Repository configuration
        """
        return {
            "user_repository": {
                "type": "dynamodb",
                "table_name": settings.aws_dynamodb_table,
                "instance_created": cls._user_repository_instance is not None
            }
        } 