from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import structlog
from contextlib import asynccontextmanager

from config import settings
from api.src.routers import health_router, user_router, test_router

# Configuración de logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    logger.info("Starting application", app_name=settings.app_name)
    
    # Here you can add AWS services, database initialization, etc.
    
    yield
    
    # Shutdown
    logger.info("Shutting down application", app_name=settings.app_name)


# Create FastAPI instance
app = FastAPI(
    title=settings.app_name,
    description="Backend API with hexagonal architecture and AWS services",
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Trusted Hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

# Include routers
app.include_router(health_router.router, prefix="/api/v1", tags=["health"])
app.include_router(user_router.router, prefix="/api/v1", tags=["users"])
app.include_router(test_router.router, prefix="/api/v1", tags=["test"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.version
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    ) 