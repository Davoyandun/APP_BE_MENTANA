"""
Use Case Factory for APP_BE_MENTANA

This factory centralizes the creation of use case instances,
making it easier to manage business logic dependencies and configurations.
"""

from typing import Optional
from domain.src.use_cases.create_user_use_case import CreateUserUseCase
from domain.src.use_cases.get_user_use_case import GetUserUseCase
from domain.src.use_cases.get_all_users_use_case import GetAllUsersUseCase
from domain.src.repositories.user_repository import UserRepository
from factories.repository_factory import RepositoryFactory
import structlog

logger = structlog.get_logger()


class UseCaseFactory:
    """
    Factory for creating use case instances.
    
    This factory follows the Factory pattern to centralize use case creation
    and make it easier to manage business logic dependencies.
    """
    
    _create_user_use_case_instance: Optional[CreateUserUseCase] = None
    _get_user_use_case_instance: Optional[GetUserUseCase] = None
    _get_all_users_use_case_instance: Optional[GetAllUsersUseCase] = None
    
    @classmethod
    def create_create_user_use_case(cls, user_repository: UserRepository = None) -> CreateUserUseCase:
        """
        Creates and returns a CreateUserUseCase instance.
        
        Args:
            user_repository: Optional user repository instance. If not provided,
                           will use the default from RepositoryFactory.
        
        Returns:
            CreateUserUseCase: Configured use case instance
        """
        if cls._create_user_use_case_instance is None:
            logger.info("Creating new CreateUserUseCase instance")
            
            # Get repository instance if not provided
            if user_repository is None:
                user_repository = RepositoryFactory.get_user_repository()
            
            # Create use case instance
            cls._create_user_use_case_instance = CreateUserUseCase(
                user_repository=user_repository
            )
            
            logger.info("CreateUserUseCase instance created")
        
        return cls._create_user_use_case_instance
    
    @classmethod
    def get_create_user_use_case(cls) -> CreateUserUseCase:
        """
        Gets the existing CreateUserUseCase instance or creates a new one.
        
        Returns:
            CreateUserUseCase: Use case instance
        """
        return cls.create_create_user_use_case()
    
    @classmethod
    def create_get_user_use_case(cls, user_repository: UserRepository = None) -> GetUserUseCase:
        """
        Creates and returns a GetUserUseCase instance.
        
        Args:
            user_repository: Optional user repository instance. If not provided,
                           will use the default from RepositoryFactory.
        
        Returns:
            GetUserUseCase: Configured use case instance
        """
        if cls._get_user_use_case_instance is None:
            logger.info("Creating new GetUserUseCase instance")
            
            # Get repository instance if not provided
            if user_repository is None:
                user_repository = RepositoryFactory.get_user_repository()
            
            # Create use case instance
            cls._get_user_use_case_instance = GetUserUseCase(
                user_repository=user_repository
            )
            
            logger.info("GetUserUseCase instance created")
        
        return cls._get_user_use_case_instance
    
    @classmethod
    def get_get_user_use_case(cls) -> GetUserUseCase:
        """
        Gets the existing GetUserUseCase instance or creates a new one.
        
        Returns:
            GetUserUseCase: Use case instance
        """
        return cls.create_get_user_use_case()
    
    @classmethod
    def create_get_all_users_use_case(cls, user_repository: UserRepository = None) -> GetAllUsersUseCase:
        """
        Creates and returns a GetAllUsersUseCase instance.
        
        Args:
            user_repository: Optional user repository instance. If not provided,
                           will use the default from RepositoryFactory.
        
        Returns:
            GetAllUsersUseCase: Configured use case instance
        """
        if cls._get_all_users_use_case_instance is None:
            logger.info("Creating new GetAllUsersUseCase instance")
            
            # Get repository instance if not provided
            if user_repository is None:
                user_repository = RepositoryFactory.get_user_repository()
            
            # Create use case instance
            cls._get_all_users_use_case_instance = GetAllUsersUseCase(
                user_repository=user_repository
            )
            
            logger.info("GetAllUsersUseCase instance created")
        
        return cls._get_all_users_use_case_instance
    
    @classmethod
    def get_get_all_users_use_case(cls) -> GetAllUsersUseCase:
        """
        Gets the existing GetAllUsersUseCase instance or creates a new one.
        
        Returns:
            GetAllUsersUseCase: Use case instance
        """
        return cls.create_get_all_users_use_case()
    
    @classmethod
    def reset_create_user_use_case(cls):
        """
        Resets the CreateUserUseCase instance (useful for testing).
        """
        cls._create_user_use_case_instance = None
        logger.info("CreateUserUseCase instance reset")
    
    @classmethod
    def reset_get_user_use_case(cls):
        """
        Resets the GetUserUseCase instance (useful for testing).
        """
        cls._get_user_use_case_instance = None
        logger.info("GetUserUseCase instance reset")
    
    @classmethod
    def reset_get_all_users_use_case(cls):
        """
        Resets the GetAllUsersUseCase instance (useful for testing).
        """
        cls._get_all_users_use_case_instance = None
        logger.info("GetAllUsersUseCase instance reset")
    
    @classmethod
    def create_use_case_with_repository(cls, use_case_type: str, repository_type: str = "dynamodb", **kwargs):
        """
        Creates a use case instance with a specific repository type.
        
        Args:
            use_case_type: Type of use case to create
            repository_type: Type of repository to use
            **kwargs: Additional configuration parameters
            
        Returns:
            Use case instance
            
        Raises:
            ValueError: If use case type is not supported
        """
        if use_case_type.lower() == "create_user":
            # Create repository based on type
            user_repository = RepositoryFactory.create_repository_by_type(
                repository_type, **kwargs
            )
            
            # Create use case with the repository
            return CreateUserUseCase(user_repository=user_repository)
        
        elif use_case_type.lower() == "get_user":
            # Create repository based on type
            user_repository = RepositoryFactory.create_repository_by_type(
                repository_type, **kwargs
            )
            
            # Create use case with the repository
            return GetUserUseCase(user_repository=user_repository)
        
        elif use_case_type.lower() == "get_all_users":
            # Create repository based on type
            user_repository = RepositoryFactory.create_repository_by_type(
                repository_type, **kwargs
            )
            
            # Create use case with the repository
            return GetAllUsersUseCase(user_repository=user_repository)
        
        else:
            raise ValueError(f"Unsupported use case type: {use_case_type}")
    
    @classmethod
    def get_use_case_config(cls) -> dict:
        """
        Returns the current use case configuration.
        
        Returns:
            dict: Use case configuration
        """
        return {
            "create_user_use_case": {
                "type": "CreateUserUseCase",
                "instance_created": cls._create_user_use_case_instance is not None,
                "dependencies": ["UserRepository"]
            },
            "get_user_use_case": {
                "type": "GetUserUseCase",
                "instance_created": cls._get_user_use_case_instance is not None,
                "dependencies": ["UserRepository"]
            },
            "get_all_users_use_case": {
                "type": "GetAllUsersUseCase",
                "instance_created": cls._get_all_users_use_case_instance is not None,
                "dependencies": ["UserRepository"]
            }
        }
    
    @classmethod
    def create_all_use_cases(cls) -> dict:
        """
        Creates all configured use cases and returns them in a dictionary.
        
        Returns:
            dict: Dictionary containing all use case instances
        """
        use_cases = {}
        
        try:
            use_cases["create_user"] = cls.create_create_user_use_case()
        except Exception as e:
            logger.warning("Failed to create CreateUserUseCase", error=str(e))
        
        try:
            use_cases["get_user"] = cls.create_get_user_use_case()
        except Exception as e:
            logger.warning("Failed to create GetUserUseCase", error=str(e))
        
        try:
            use_cases["get_all_users"] = cls.create_get_all_users_use_case()
        except Exception as e:
            logger.warning("Failed to create GetAllUsersUseCase", error=str(e))
        
        return use_cases
    
    @classmethod
    def reset_all_use_cases(cls):
        """
        Resets all use case instances (useful for testing).
        """
        cls.reset_create_user_use_case()
        cls.reset_get_user_use_case()
        cls.reset_get_all_users_use_case()
        logger.info("All use case instances reset") 