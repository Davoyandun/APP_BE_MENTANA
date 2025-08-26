from abc import ABC, abstractmethod
from typing import Optional


class FileStorageService(ABC):
    """File storage service interface - domain port"""
    
    @abstractmethod
    async def upload_file(self, key: str, content: bytes, content_type: Optional[str] = None) -> str:
        """Uploads a file and returns the URL"""
        pass
    
    @abstractmethod
    async def get_file_url(self, key: str) -> str:
        """Gets the URL for a file"""
        pass
    
    @abstractmethod
    async def delete_file(self, key: str) -> bool:
        """Deletes a file"""
        pass
    
    @abstractmethod
    async def file_exists(self, key: str) -> bool:
        """Checks if a file exists"""
        pass 