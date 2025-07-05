from typing import List

from domain.src.entities.user import User
from domain.src.repositories.user_repository import UserRepository


class GetAllUsersUseCase:
    """Use case for getting all users"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self) -> List[User]:
        """
        Executes the use case to get all users
        
        Returns:
            List[User]: List of all users
        """
        return await self.user_repository.find_all() 