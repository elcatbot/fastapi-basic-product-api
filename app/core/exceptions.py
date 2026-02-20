from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging

class DomainException(Exception):
    """Base class for all business logic errors"""
    pass

class EntityNotFoundError(DomainException):
    """Raised when a record is not found in the DB"""
    def __init__(self, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id

# Set up logging to see the errors in your console
logger = logging.getLogger("app")

async def global_exception_handler(request: Request, exc: Exception):
    # Log the full error for the developer
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": request.url.path
        },
    )

async def sqlalchemy_integrity_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Database Constraint Violated",
            "detail": str(exc.orig) if hasattr(exc, 'orig') else "Duplicate or invalid data"
        }
    )

async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Resource Not Found",
            "message": f"{exc.entity_name} with id {exc.entity_id} does not exist.",
            "code": "ENTITY_NOT_FOUND"
        }
    )

