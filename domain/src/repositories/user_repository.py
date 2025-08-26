from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.src.entities.user import User


class UserRepository(ABC):
    """User repository interface - domain port"""
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Saves a user"""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Finds a user by ID"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Finds a user by email"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[User]:
        """Gets all users"""
        pass
    
    @abstractmethod
    async def find_active_users(self) -> List[User]:
        """Gets all active users"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Deletes a user"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Updates a user"""
        pass 