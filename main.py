from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from core.build import AppBuilder
import logging

# Import logger configuration
from utils.logger_config import logger

# Configure logging to use loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Convert logging records to loguru
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname.lower(), record.getMessage())

# Replace default logging configuration
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request details
        logger.info(f"Request started - {request.method} {request.url.path} from {request.client.host}")

        # Proceed to the next middleware or request handler
        response = await call_next(request)

        process_time = time.time() - start_time

        # Log response details and processing time
        logger.info(f"Request completed - {request.method} {request.url.path} - Status: {response.status_code} - "
                    f"Time: {process_time:.4f}s")

        return response

app = AppBuilder().get_app()
app.add_middleware(LogMiddleware)