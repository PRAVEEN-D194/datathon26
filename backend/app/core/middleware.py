import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.logging import logger
from collections import defaultdict

class RateLimiter:
    def __init__(self, limit: int, period: int):
        self.limit = limit
        self.period = period
        # Simple memory limit tracking: client_ip -> list of timestamps
        self.requests = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        # Filter out timestamps older than the period
        self.requests[client_ip] = [t for t in self.requests[client_ip] if now - t < self.period]
        
        if len(self.requests[client_ip]) >= self.limit:
            return False
            
        self.requests[client_ip].append(now)
        return True

rate_limiter = RateLimiter(limit=settings.RATE_LIMIT_CALLS, period=settings.RATE_LIMIT_PERIOD_SECONDS)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request basic details
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"Incoming request: {request.method} {request.url.path} from IP {client_ip}")

        # Basic rate limiting
        if not rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for IP {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
            
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.info(f"Completed request: {request.method} {request.url.path} - Status: {response.status_code} in {process_time:.4f}s")
            return response
        except Exception as e:
            logger.error(f"Request failed: {request.method} {request.url.path} - Error: {str(e)}")
            raise e
