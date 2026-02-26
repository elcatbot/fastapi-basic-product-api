from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.core.logging_config import logger
import logging

class DomainException(Exception):
    """Base class for all business logic errors"""
    pass

class EntityNotFoundError(DomainException):
    """Raised when a record is not found in the DB"""
    def __init__(self, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id

# # Set up logging to see the errors in your console
# logger = logging.getLogger("app")

async def global_exception_handler(request: Request, exc: Exception):
    # Log the full error for the developer
    logger.error(f"UNHANDLED ERROR: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": request.url.path
        },
    )

async def sqlalchemy_integrity_handler(request: Request, exc: IntegrityError):
    # This writes to BOTH the console and logs/app.log
    logger.error(f"DATABASE ERROR: {exc.orig} | Path: {request.url.path}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Database Constraint Violated",
            "detail": str(exc.orig) if hasattr(exc, 'orig') else "Duplicate or invalid data"
        }
    )

async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    # This writes to BOTH the console and logs/app.log
    logger.error(f"ENTITY_NOT_FOUND ERROR: {exc.entity_name} with id {exc.entity_id} does not exist | Path: {request.url.path}")

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Resource Not Found",
            "message": f"{exc.entity_name} with id {exc.entity_id} does not exist.",
            "code": "ENTITY_NOT_FOUND"
        }
    )

