"""Request logging and error handling middleware."""

import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from app.core.logging import get_logger
from app.core.exceptions import SloozeException

logger = get_logger("middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request with timing, method, path, and status."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Attach request ID to state
        request.state.request_id = request_id

        logger.info(
            "request_started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else "unknown",
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration = round((time.time() - start_time) * 1000, 2)
            logger.error(
                "request_failed",
                request_id=request_id,
                error=str(exc),
                duration_ms=duration,
            )
            raise

        duration = round((time.time() - start_time) * 1000, 2)

        logger.info(
            "request_completed",
            request_id=request_id,
            status_code=response.status_code,
            duration_ms=duration,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration}ms"

        return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Catches SloozeException and returns structured JSON errors."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except SloozeException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": type(exc).__name__,
                    "message": exc.message,
                    "success": False,
                },
            )
        except Exception as exc:
            logger.error("unhandled_exception", error=str(exc), exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "success": False,
                },
            )
