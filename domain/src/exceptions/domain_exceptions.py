class DomainException(Exception):
    """Base exception for domain layer"""
    pass


class UserNotFoundException(DomainException):
    """Raised when a user is not found"""
    pass


class UserAlreadyExistsException(DomainException):
    """Raised when trying to create a user that already exists"""
    pass


class InvalidUserDataException(DomainException):
    """Raised when user data is invalid"""
    pass


class FileStorageException(DomainException):
    """Raised when there's an error with file storage operations"""
    pass 