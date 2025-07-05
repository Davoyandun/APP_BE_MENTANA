from typing import Optional
from uuid import UUID

from domain.src.entities.user import User
from domain.src.repositories.user_repository import UserRepository
from domain.src.exceptions.domain_exceptions import UserNotFoundException


class GetUserUseCase:
    """Use case for getting a user by ID"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> User:
        """
        Executes the use case to get a user by ID
        
        Args:
            user_id: User's ID
            
        Returns:
            User: User if found
            
        Raises:
            UserNotFoundException: If user is not found
        """
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return user 