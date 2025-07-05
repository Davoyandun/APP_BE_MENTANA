import boto3
from typing import Optional, BinaryIO
import structlog
from config import get_aws_config
from domain.src.services.file_storage_service import FileStorageService

logger = structlog.get_logger()


class AWSS3Service(FileStorageService):
    """Service for interacting with AWS S3"""
    
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', **get_aws_config())
        self.s3_resource = boto3.resource('s3', **get_aws_config())
    
    async def upload_file(self, key: str, content: bytes, content_type: Optional[str] = None) -> str:
        """
        Uploads a file to S3
        
        Args:
            key: S3 key
            content: File content as bytes
            content_type: File content type
            
        Returns:
            str: S3 file URL
        """
        try:
            import io
            file_obj = io.BytesIO(content)
            
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs=extra_args
            )
            
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{key}"
            logger.info("File uploaded successfully to S3", key=key, url=url)
            
            return url
            
        except Exception as e:
            logger.error("Error uploading file to S3", error=str(e), key=key)
            raise Exception(f"Error uploading file to S3: {str(e)}")
    
    async def upload_fileobj(self, file_obj: BinaryIO, s3_key: str, content_type: Optional[str] = None) -> str:
        """
        Uploads a file object to S3
        
        Args:
            file_obj: File object
            s3_key: S3 key
            content_type: File content type
            
        Returns:
            str: S3 file URL
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )
            
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            logger.info("File uploaded successfully to S3", s3_key=s3_key, url=url)
            
            return url
            
        except Exception as e:
            logger.error("Error uploading file to S3", error=str(e), s3_key=s3_key)
            raise Exception(f"Error uploading file to S3: {str(e)}")
    
    async def download_file(self, s3_key: str, local_path: str) -> str:
        """
        Downloads a file from S3
        
        Args:
            s3_key: S3 key
            local_path: Local path to save the file
            
        Returns:
            str: Local path of downloaded file
        """
        try:
            self.s3_client.download_file(
                self.bucket_name,
                s3_key,
                local_path
            )
            
            logger.info("File downloaded successfully from S3", s3_key=s3_key, local_path=local_path)
            
            return local_path
            
        except Exception as e:
            logger.error("Error downloading file from S3", error=str(e), s3_key=s3_key)
            raise Exception(f"Error downloading file from S3: {str(e)}")
    
    async def delete_file(self, key: str) -> bool:
        """
        Deletes a file from S3
        
        Args:
            key: S3 key
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            logger.info("File deleted successfully from S3", key=key)
            
            return True
            
        except Exception as e:
            logger.error("Error deleting file from S3", error=str(e), key=key)
            raise Exception(f"Error deleting file from S3: {str(e)}")
    
    async def get_file_url(self, key: str) -> str:
        """
        Gets the URL for a file
        
        Args:
            key: S3 key
            
        Returns:
            str: File URL
        """
        try:
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{key}"
            logger.info("File URL generated successfully", key=key, url=url)
            
            return url
            
        except Exception as e:
            logger.error("Error generating file URL", error=str(e), key=key)
            raise Exception(f"Error generating file URL: {str(e)}")
    
    async def file_exists(self, key: str) -> bool:
        """
        Checks if a file exists in S3
        
        Args:
            key: S3 key
            
        Returns:
            bool: True if file exists
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            return True
            
        except Exception:
            return False 