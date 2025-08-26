from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, List
import structlog
import asyncio
from datetime import datetime, timezone
import uuid

from config import settings
from domain.src.repositories.user_repository import UserRepository
from domain.src.use_cases.create_user_use_case import CreateUserUseCase
from domain.src.use_cases.get_all_users_use_case import GetAllUsersUseCase
from domain.src.services.file_storage_service import FileStorageService
from adapters.services.aws_s3_service import AWSS3Service
from domain.src.entities.user import User
from factories.repository_factory import RepositoryFactory
from factories.service_factory import ServiceFactory
from factories.use_case_factory import UseCaseFactory
from factories.user_factory import UserFactory

logger = structlog.get_logger()
router = APIRouter()


def get_user_repository() -> UserRepository:
    """Dependency injection for user repository using factory"""
    return RepositoryFactory.get_user_repository()


def get_s3_service() -> FileStorageService:
    """Dependency injection for S3 service using factory"""
    return ServiceFactory.get_s3_service()


def get_create_user_use_case() -> CreateUserUseCase:
    """Dependency injection for create user use case using factory"""
    return UseCaseFactory.get_create_user_use_case()


def get_get_all_users_use_case() -> GetAllUsersUseCase:
    """Dependency injection for get all users use case using factory"""
    return UseCaseFactory.get_get_all_users_use_case()


@router.get("/test/health")
async def test_health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint that tests all system components
    """
    try:
        logger.info("Comprehensive health check requested")
        
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "app_info": {
                "name": settings.app_name,
                "version": settings.version,
                "environment": "development" if settings.debug else "production"
            },
            "services": {
                "api": "healthy",
                "dynamodb": "unknown",
                "s3": "unknown",
                "aws_credentials": "unknown"
            },
            "system": {
                "python_version": f"{settings.python_version}",
                "fastapi_version": "0.104.1",
                "uvicorn_version": "0.24.0"
            }
        }
        
        # Test AWS credentials
        try:
            import boto3
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            health_status["services"]["aws_credentials"] = "healthy"
            health_status["aws_info"] = {
                "account_id": identity.get('Account'),
                "user_arn": identity.get('Arn'),
                "user_id": identity.get('UserId')
            }
        except Exception as e:
            logger.warning("AWS credentials test failed", error=str(e))
            health_status["services"]["aws_credentials"] = "unhealthy"
            health_status["aws_error"] = str(e)
        
        # Test DynamoDB connection
        try:
            user_repo = RepositoryFactory.get_user_repository()
            # Try to list tables or perform a simple operation
            import boto3
            dynamodb = boto3.client('dynamodb')
            tables = dynamodb.list_tables()
            health_status["services"]["dynamodb"] = "healthy"
            health_status["dynamodb_info"] = {
                "table_name": settings.aws_dynamodb_table,
                "tables_available": len(tables.get('TableNames', []))
            }
        except Exception as e:
            logger.warning("DynamoDB test failed", error=str(e))
            health_status["services"]["dynamodb"] = "unhealthy"
            health_status["dynamodb_error"] = str(e)
        
        # Test S3 connection
        try:
            s3_service = ServiceFactory.get_s3_service()
            # Try to list buckets or perform a simple operation
            import boto3
            s3 = boto3.client('s3')
            buckets = s3.list_buckets()
            health_status["services"]["s3"] = "healthy"
            health_status["s3_info"] = {
                "bucket_name": settings.aws_s3_bucket,
                "buckets_available": len(buckets.get('Buckets', []))
            }
        except Exception as e:
            logger.warning("S3 test failed", error=str(e))
            health_status["services"]["s3"] = "unhealthy"
            health_status["s3_error"] = str(e)
        
        # Determine overall status
        unhealthy_services = [
            service for service, status in health_status["services"].items()
            if status == "unhealthy"
        ]
        
        if unhealthy_services:
            health_status["status"] = "degraded"
            health_status["unhealthy_services"] = unhealthy_services
        
        logger.info("Health check completed", status=health_status["status"])
        return health_status
        
    except Exception as e:
        logger.error("Error in comprehensive health check", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")


@router.post("/test/user")
async def test_user_creation(
    background_tasks: BackgroundTasks,
    create_user_use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> Dict[str, Any]:
    """
    Test endpoint that creates a test user and demonstrates the hexagonal architecture
    """
    try:
        logger.info("Test user creation requested")
        
        # Create test user data
        test_email = f"test-{uuid.uuid4().hex[:8]}@example.com"
        test_name = "Test User"
        
        # Execute use case (domain layer)
        user = await create_user_use_case.execute(
            email=test_email,
            name=test_name
        )
        
        # Add background task to demonstrate async processing
        background_tasks.add_task(log_test_user_creation, str(user.id))
        
        result = {
            "message": "Test user created successfully",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            },
            "architecture_demo": {
                "domain_layer": "User entity created with business logic",
                "use_case_layer": "CreateUserUseCase executed successfully",
                "adapter_layer": "AWSDynamoDBUserRepository saved to DynamoDB",
                "hexagonal_architecture": "Ports and adapters pattern demonstrated"
            }
        }
        
        logger.info("Test user created successfully", user_id=str(user.id))
        return result
        
    except ValueError as e:
        logger.warning("Validation error in test user creation", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Error in test user creation", error=str(e))
        raise HTTPException(status_code=500, detail="Test user creation failed")


@router.get("/test/users")
async def test_user_retrieval(
    get_all_users_use_case: GetAllUsersUseCase = Depends(get_get_all_users_use_case)
) -> Dict[str, Any]:
    """
    Test endpoint that retrieves all users and demonstrates repository pattern
    """
    try:
        logger.info("Test user retrieval requested")
        
        # Retrieve all users using use case
        users = await get_all_users_use_case.execute()
        
        user_list = [
            {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            }
            for user in users
        ]
        
        result = {
            "message": f"Retrieved {len(user_list)} users successfully",
            "users": user_list,
            "total_count": len(user_list),
            "repository_demo": {
                "repository_interface": "UserRepository interface used",
                "repository_implementation": "AWSDynamoDBUserRepository executed",
                "data_persistence": "DynamoDB query executed successfully"
            }
        }
        
        logger.info("Test user retrieval completed", count=len(user_list))
        return result
        
    except Exception as e:
        logger.error("Error in test user retrieval", error=str(e))
        raise HTTPException(status_code=500, detail="Test user retrieval failed")


@router.post("/test/s3")
async def test_s3_operations(
    s3_service: FileStorageService = Depends(get_s3_service)
) -> Dict[str, Any]:
    """
    Test endpoint that demonstrates S3 service operations
    """
    try:
        logger.info("Test S3 operations requested")
        
        # Create test file content
        test_content = f"Test file created at {datetime.now(timezone.utc).isoformat()}"
        test_key = f"test-files/test-{uuid.uuid4().hex[:8]}.txt"
        
        # Upload file to S3
        await s3_service.upload_file(
            key=test_key,
            content=test_content.encode('utf-8'),
            content_type="text/plain"
        )
        
        # Get file URL
        file_url = await s3_service.get_file_url(test_key)
        
        result = {
            "message": "S3 operations completed successfully",
            "s3_operations": {
                "file_uploaded": test_key,
                "file_url": file_url,
                "content_length": len(test_content)
            },
            "service_demo": {
                "service_interface": "S3Service interface used",
                "service_implementation": "AWSS3Service executed",
                "aws_integration": "S3 operations completed successfully"
            }
        }
        
        logger.info("Test S3 operations completed", file_key=test_key)
        return result
        
    except Exception as e:
        logger.error("Error in test S3 operations", error=str(e))
        raise HTTPException(status_code=500, detail="Test S3 operations failed")


@router.get("/test/architecture")
async def test_architecture_demo() -> Dict[str, Any]:
    """
    Test endpoint that demonstrates the hexagonal architecture concepts
    """
    try:
        logger.info("Architecture demo requested")
        
        architecture_demo = {
            "hexagonal_architecture": {
                "description": "Ports and Adapters Architecture",
                "benefits": [
                    "Separation of concerns",
                    "Testability",
                    "Independence of frameworks",
                    "Independence of UI",
                    "Independence of Database",
                    "Independence of any external agency"
                ]
            },
            "layers": {
                "domain_layer": {
                    "description": "Business logic and entities",
                    "components": ["User entity", "Repository interfaces", "Use cases"],
                    "location": "domain/src/"
                },
                "application_layer": {
                    "description": "API controllers and DTOs",
                    "components": ["Routers", "DTOs", "Exception handlers"],
                    "location": "api/src/"
                },
                "infrastructure_layer": {
                    "description": "External services and implementations",
                    "components": ["AWS DynamoDB Repository", "AWS S3 Service"],
                    "location": "adapters/"
                }
            },
            "dependency_injection": {
                "description": "Dependencies are injected through FastAPI's Depends",
                "example": "get_user_repository() function provides repository instances"
            },
            "ports_and_adapters": {
                "ports": "Interfaces (UserRepository, S3Service)",
                "adapters": "Implementations (AWSDynamoDBUserRepository, AWSS3Service)"
            }
        }
        
        return {
            "message": "Architecture demonstration",
            "architecture": architecture_demo,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error("Error in architecture demo", error=str(e))
        raise HTTPException(status_code=500, detail="Architecture demo failed")


@router.get("/test/performance")
async def test_performance() -> Dict[str, Any]:
    """
    Test endpoint that demonstrates performance monitoring
    """
    try:
        logger.info("Performance test requested")
        
        import time
        start_time = time.time()
        
        # Simulate some work
        await asyncio.sleep(0.1)
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        performance_metrics = {
            "execution_time_ms": round(execution_time, 2),
            "memory_usage": "Available through monitoring tools",
            "cpu_usage": "Available through monitoring tools",
            "response_time": "Measured from client perspective"
        }
        
        result = {
            "message": "Performance test completed",
            "metrics": performance_metrics,
            "recommendations": [
                "Use async/await for I/O operations",
                "Implement caching for frequently accessed data",
                "Monitor database query performance",
                "Use connection pooling for database connections"
            ]
        }
        
        logger.info("Performance test completed", execution_time_ms=execution_time)
        return result
        
    except Exception as e:
        logger.error("Error in performance test", error=str(e))
        raise HTTPException(status_code=500, detail="Performance test failed")


async def log_test_user_creation(user_id: str):
    """Background task to log user creation"""
    await asyncio.sleep(1)  # Simulate some async work
    logger.info("Background task: Test user creation logged", user_id=user_id)


@router.get("/test/factories")
async def test_factories_demo() -> Dict[str, Any]:
    """
    Test endpoint that demonstrates the Factory pattern implementation
    """
    try:
        logger.info("Factory pattern demo requested")
        
        # Demonstrate factory usage
        factory_demo = {
            "factory_pattern": {
                "description": "Centralized object creation and dependency management",
                "benefits": [
                    "Centralized configuration",
                    "Easier testing and mocking",
                    "Dependency injection management",
                    "Consistent object creation",
                    "Easy switching between implementations"
                ]
            },
            "factories_implemented": {
                "RepositoryFactory": {
                    "description": "Creates repository instances",
                    "methods": [
                        "create_user_repository()",
                        "get_user_repository()",
                        "create_repository_by_type()",
                        "reset_user_repository()"
                    ],
                    "config": RepositoryFactory.get_repository_config()
                },
                "ServiceFactory": {
                    "description": "Creates service instances",
                    "methods": [
                        "create_s3_service()",
                        "get_s3_service()",
                        "create_service_by_type()",
                        "reset_s3_service()"
                    ],
                    "config": ServiceFactory.get_service_config()
                },
                "UseCaseFactory": {
                    "description": "Creates use case instances",
                    "methods": [
                        "create_create_user_use_case()",
                        "get_create_user_use_case()",
                        "create_use_case_with_repository()",
                        "reset_create_user_use_case()"
                    ],
                    "config": UseCaseFactory.get_use_case_config()
                },
                "UserFactory": {
                    "description": "Creates user entities",
                    "methods": [
                        "create_user()",
                        "create_test_user()",
                        "create_user_from_dict()",
                        "validate_user_data()"
                    ],
                    "template": UserFactory.get_user_template()
                }
            },
            "factory_usage_examples": {
                "repository_creation": "RepositoryFactory.get_user_repository()",
                "service_creation": "ServiceFactory.get_s3_service()",
                "use_case_creation": "UseCaseFactory.get_create_user_use_case()",
                "user_creation": "UserFactory.create_test_user()"
            }
        }
        
        return {
            "message": "Factory pattern demonstration",
            "factories": factory_demo,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error("Error in factory pattern demo", error=str(e))
        raise HTTPException(status_code=500, detail="Factory pattern demo failed")


@router.delete("/test/cleanup")
async def test_cleanup(
    user_repository: UserRepository = Depends(get_user_repository),
    s3_service: FileStorageService = Depends(get_s3_service)
) -> Dict[str, Any]:
    """
    Test endpoint to cleanup test data (use with caution in production)
    """
    try:
        logger.info("Test cleanup requested")
        
        # This is a demo endpoint - in production, you'd want more sophisticated cleanup
        cleanup_result = {
            "message": "Cleanup completed (demo mode)",
            "note": "In production, implement proper cleanup strategies",
            "recommendations": [
                "Use database transactions for cleanup",
                "Implement soft deletes where appropriate",
                "Archive data instead of permanent deletion",
                "Use scheduled cleanup jobs"
            ]
        }
        
        logger.info("Test cleanup completed")
        return cleanup_result
        
    except Exception as e:
        logger.error("Error in test cleanup", error=str(e))
        raise HTTPException(status_code=500, detail="Test cleanup failed") 