"""
User Factory for APP_BE_MENTANA

This factory centralizes the creation of user entities,
making it easier to manage user object creation and validation.
"""

from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4
from domain.src.entities.user import User
import structlog

logger = structlog.get_logger()


class UserFactory:
    """
    Factory for creating user entities.
    
    This factory follows the Factory pattern to centralize user creation
    and make it easier to manage user object creation and validation.
    """
    
    @classmethod
    def create_user(cls, email: str, name: str, is_active: bool = True) -> User:
        """
        Creates a new user entity with the provided data.
        
        Args:
            email: User's email address
            name: User's name
            is_active: Whether the user is active (default: True)
        
        Returns:
            User: New user entity instance
            
        Raises:
            ValueError: If email or name is invalid
        """
        logger.info("Creating new user entity", email=email, name=name)
        
        # Validate input
        if not email or not email.strip():
            raise ValueError("Email is required")
        
        if not name or not name.strip():
            raise ValueError("Name is required")
        
        # Create user entity
        user = User(
            id=uuid4(),
            email=email.strip().lower(),
            name=name.strip(),
            is_active=is_active,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        logger.info("User entity created successfully", user_id=str(user.id))
        return user
    
    @classmethod
    def create_test_user(cls, prefix: str = "test") -> User:
        """
        Creates a test user with generated data.
        
        Args:
            prefix: Prefix for the test user data (default: "test")
        
        Returns:
            User: Test user entity instance
        """
        timestamp = int(datetime.now(timezone.utc).timestamp())
        email = f"{prefix}-{timestamp}@example.com"
        name = f"{prefix.title()} User {timestamp}"
        
        return cls.create_user(email=email, name=name)
    
    @classmethod
    def create_user_from_dict(cls, user_data: dict) -> User:
        """
        Creates a user entity from a dictionary.
        
        Args:
            user_data: Dictionary containing user data
        
        Returns:
            User: User entity instance
            
        Raises:
            ValueError: If required data is missing or invalid
        """
        # Extract data with defaults
        email = user_data.get("email")
        name = user_data.get("name")
        is_active = user_data.get("is_active", True)
        
        # Create user
        return cls.create_user(email=email, name=name, is_active=is_active)
    
    @classmethod
    def create_user_with_id(cls, user_id: str, email: str, name: str, 
                           is_active: bool = True, created_at: Optional[datetime] = None,
                           updated_at: Optional[datetime] = None) -> User:
        """
        Creates a user entity with a specific ID (useful for testing or data migration).
        
        Args:
            user_id: Specific user ID
            email: User's email address
            name: User's name
            is_active: Whether the user is active
            created_at: Creation timestamp
            updated_at: Last update timestamp
        
        Returns:
            User: User entity instance
        """
        logger.info("Creating user entity with specific ID", user_id=user_id)
        
        # Validate input
        if not email or not email.strip():
            raise ValueError("Email is required")
        
        if not name or not name.strip():
            raise ValueError("Name is required")
        
        # Parse user ID
        try:
            from uuid import UUID
            parsed_id = UUID(user_id)
        except ValueError:
            raise ValueError("Invalid user ID format")
        
        # Set timestamps
        now = datetime.now(timezone.utc)
        created_at = created_at or now
        updated_at = updated_at or now
        
        # Create user entity
        user = User(
            id=parsed_id,
            email=email.strip().lower(),
            name=name.strip(),
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
        
        logger.info("User entity created with specific ID", user_id=str(user.id))
        return user
    
    @classmethod
    def validate_user_data(cls, user_data: dict) -> dict:
        """
        Validates user data and returns cleaned data.
        
        Args:
            user_data: Dictionary containing user data
        
        Returns:
            dict: Cleaned and validated user data
            
        Raises:
            ValueError: If data is invalid
        """
        errors = []
        cleaned_data = {}
        
        # Validate email
        email = user_data.get("email", "").strip()
        if not email:
            errors.append("Email is required")
        elif "@" not in email:
            errors.append("Invalid email format")
        else:
            cleaned_data["email"] = email.lower()
        
        # Validate name
        name = user_data.get("name", "").strip()
        if not name:
            errors.append("Name is required")
        elif len(name) < 2:
            errors.append("Name must be at least 2 characters long")
        else:
            cleaned_data["name"] = name
        
        # Validate is_active
        is_active = user_data.get("is_active")
        if is_active is not None and not isinstance(is_active, bool):
            errors.append("is_active must be a boolean")
        else:
            cleaned_data["is_active"] = is_active if is_active is not None else True
        
        if errors:
            raise ValueError(f"Validation errors: {', '.join(errors)}")
        
        return cleaned_data
    
    @classmethod
    def get_user_template(cls) -> dict:
        """
        Returns a template for user data structure.
        
        Returns:
            dict: User data template
        """
        return {
            "email": "user@example.com",
            "name": "User Name",
            "is_active": True
        }
 