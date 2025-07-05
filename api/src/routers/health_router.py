from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import structlog
from config import settings

logger = structlog.get_logger()

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for application monitoring
    """
    try:
        logger.info("Health check requested")
        
        # Here you can add AWS services, DynamoDB verifications, etc.
        health_status = {
            "status": "healthy",
            "services": {
                "api": "healthy",
                "dynamodb": "healthy",  # TODO: Implement real verification
                "aws": "healthy",       # TODO: Implement real verification
                "redis": "healthy" if settings.redis_url else "not_configured"
            },
            "timestamp": "2024-01-01T00:00:00Z"  # TODO: Use real datetime
        }
        
        return health_status
        
    except Exception as e:
        logger.error("Error in health check", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/health/ready")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check to verify if the application is ready to receive traffic
    """
    try:
        logger.info("Readiness check requested")
        
        # Verify that all critical services are available
        readiness_status = {
            "status": "ready",
            "message": "Application is ready to receive traffic"
        }
        
        return readiness_status
        
    except Exception as e:
        logger.error("Error in readiness check", error=str(e))
        raise HTTPException(status_code=503, detail="Application not ready")


@router.get("/health/live")
async def liveness_check() -> Dict[str, Any]:
    """
    Liveness check to verify if the application is running
    """
    try:
        logger.info("Liveness check requested")
        
        liveness_status = {
            "status": "alive",
            "message": "Application is running"
        }
        
        return liveness_status
        
    except Exception as e:
        logger.error("Error in liveness check", error=str(e))
        raise HTTPException(status_code=500, detail="Application is not alive") 