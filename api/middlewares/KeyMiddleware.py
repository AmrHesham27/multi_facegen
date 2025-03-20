from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message
from fastapi import HTTPException, status
import os

class KeyMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next):
        await self.set_body(request)
        json_body = await request.json()

        api_key = json_body.get("key")

        if api_key is None or api_key != os.getenv('API_KEY'):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or missing API Key",
                )

        response = await call_next(request)

        return response