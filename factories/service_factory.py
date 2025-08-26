"""
Service Factory for APP_BE_MENTANA

This factory centralizes the creation of service instances,
making it easier to manage AWS service dependencies and configurations.
"""

from typing import Optional
from domain.src.services.file_storage_service import FileStorageService
from adapters.services.aws_s3_service import AWSS3Service
from config import settings
import structlog

logger = structlog.get_logger()


class ServiceFactory:
    """
    Factory for creating service instances.
    
    This factory follows the Factory pattern to centralize service creation
    and make it easier to switch between different service implementations.
    """
    
    _s3_service_instance: Optional[FileStorageService] = None
    
    @classmethod
    def create_s3_service(cls) -> FileStorageService:
        """
        Creates and returns an S3 service instance.
        
        Returns:
            FileStorageService: Configured S3 service instance
            
        Raises:
            ValueError: If S3 service configuration is invalid
        """
        if cls._s3_service_instance is None:
            logger.info("Creating new S3 service instance")
            
            # Validate configuration
            if not settings.aws_s3_bucket:
                raise ValueError("AWS S3 bucket name not configured")
            
            # Create service instance
            cls._s3_service_instance = AWSS3Service(
                bucket_name=settings.aws_s3_bucket
            )
            
            logger.info("S3 service instance created", 
                       bucket_name=settings.aws_s3_bucket)
        
        return cls._s3_service_instance
    
    @classmethod
    def get_s3_service(cls) -> FileStorageService:
        """
        Gets the existing S3 service instance or creates a new one.
        
        Returns:
            FileStorageService: S3 service instance
        """
        return cls.create_s3_service()
    
    @classmethod
    def reset_s3_service(cls):
        """
        Resets the S3 service instance (useful for testing).
        """
        cls._s3_service_instance = None
        logger.info("S3 service instance reset")
    
    @classmethod
    def create_service_by_type(cls, service_type: str, **kwargs):
        """
        Creates a service instance based on the specified type.
        
        Args:
            service_type: Type of service to create
            **kwargs: Additional configuration parameters
            
        Returns:
            Service instance
            
        Raises:
            ValueError: If service type is not supported
        """
        if service_type.lower() == "s3":
            bucket_name = kwargs.get("bucket_name", settings.aws_s3_bucket)
            if not bucket_name:
                raise ValueError("Bucket name is required for S3 service")
            
            return AWSS3Service(bucket_name=bucket_name)
        
        elif service_type.lower() == "dynamodb":
            # For future implementation of DynamoDB service
            # from adapters.services.aws_dynamodb_service import AWSDynamoDBService
            # table_name = kwargs.get("table_name", settings.aws_dynamodb_table)
            # if not table_name:
            #     raise ValueError("Table name is required for DynamoDB service")
            # 
            # return AWSDynamoDBService(table_name=table_name)
            raise ValueError("DynamoDB service not yet implemented")
        
        elif service_type.lower() == "ses":
            # For future implementation of SES service
            # from adapters.services.aws_ses_service import AWSSESService
            # region = kwargs.get("region", settings.aws_region)
            # return AWSSESService(region=region)
            raise ValueError("SES service not yet implemented")
        
        else:
            raise ValueError(f"Unsupported service type: {service_type}")
    
    @classmethod
    def get_service_config(cls) -> dict:
        """
        Returns the current service configuration.
        
        Returns:
            dict: Service configuration
        """
        return {
            "s3_service": {
                "type": "s3",
                "bucket_name": settings.aws_s3_bucket,
                "instance_created": cls._s3_service_instance is not None
            }
        }
    
    @classmethod
    def create_all_services(cls) -> dict:
        """
        Creates all configured services and returns them in a dictionary.
        
        Returns:
            dict: Dictionary containing all service instances
        """
        services = {}
        
        try:
            services["s3"] = cls.create_s3_service()
        except Exception as e:
            logger.warning("Failed to create S3 service", error=str(e))
        
        return services 