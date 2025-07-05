from typing import Optional
from uuid import UUID, uuid4

from domain.src.entities.user import User
from domain.src.repositories.user_repository import UserRepository
from domain.src.exceptions.domain_exceptions import (
    UserAlreadyExistsException,
    InvalidUserDataException
)


class CreateUserUseCase:
    """Use case for creating a new user"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, email: str, name: str) -> User:
        """
        Executes the use case to create a user
        
        Args:
            email: User's email
            name: User's name
            
        Returns:
            User: Created user
            
        Raises:
            ValueError: If email already exists or data is invalid
        """
        # Business validations
        if not email or not name:
            raise InvalidUserDataException("Email and name are required")
        
        if not self._is_valid_email(email):
            raise InvalidUserDataException("Invalid email")
        
        # Check if user already exists
        existing_user = await self.user_repository.find_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException("Email is already registered")
        
        # Create user entity
        user = User(
            id=uuid4(),  # Generate UUID explicitly
            email=email,
            name=name
        )
        
        # Save in repository
        saved_user = await self.user_repository.save(user)
        
        return saved_user
    
    def _is_valid_email(self, email: str) -> bool:
        """Validates email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None 