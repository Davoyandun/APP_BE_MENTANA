from fastapi import APIRouter, HTTPException, Depends
from typing import List
import structlog

from api.src.dtos.user_dto import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    UserListResponse
)
from domain.src.repositories.user_repository import UserRepository
from domain.src.use_cases.create_user_use_case import CreateUserUseCase
from domain.src.use_cases.get_user_use_case import GetUserUseCase
from domain.src.use_cases.get_all_users_use_case import GetAllUsersUseCase
from domain.src.exceptions.domain_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidUserDataException
)
from factories.repository_factory import RepositoryFactory
from factories.use_case_factory import UseCaseFactory

logger = structlog.get_logger()
router = APIRouter()


def get_user_repository() -> UserRepository:
    """Dependency injection for user repository using factory"""
    return RepositoryFactory.get_user_repository()


def get_create_user_use_case() -> CreateUserUseCase:
    """Dependency injection for create user use case using factory"""
    return UseCaseFactory.get_create_user_use_case()


def get_get_user_use_case() -> GetUserUseCase:
    """Dependency injection for get user use case using factory"""
    return UseCaseFactory.get_get_user_use_case()


def get_get_all_users_use_case() -> GetAllUsersUseCase:
    """Dependency injection for get all users use case using factory"""
    return UseCaseFactory.get_get_all_users_use_case()


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: CreateUserRequest,
    create_user_use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    """
    Creates a new user
    """
    try:
        logger.info("Creating user", email=user_data.email)
        
        user = await create_user_use_case.execute(
            email=user_data.email,
            name=user_data.name
        )
        
        logger.info("User created successfully", user_id=str(user.id))
        
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
    except (InvalidUserDataException, UserAlreadyExistsException) as e:
        logger.warning("Validation error creating user", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Internal error creating user", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    get_user_use_case: GetUserUseCase = Depends(get_get_user_use_case)
):
    """
    Gets a user by ID
    """
    try:
        from uuid import UUID
        
        user = await get_user_use_case.execute(UUID(user_id))
        
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
    except UserNotFoundException as e:
        logger.warning("User not found", error=str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    except Exception as e:
        logger.error("Error getting user", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users", response_model=UserListResponse)
async def get_users(
    get_all_users_use_case: GetAllUsersUseCase = Depends(get_get_all_users_use_case)
):
    """
    Gets all users
    """
    try:
        users = await get_all_users_use_case.execute()
        
        user_responses = [
            UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]
        
        return UserListResponse(
            users=user_responses,
            total=len(user_responses),
            page=1,
            size=len(user_responses)
        )
        
    except Exception as e:
        logger.error("Error getting users", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error") 