from fastapi import Request

from magicapi import g

from fastapi.responses import JSONResponse


class MagicException(Exception):
    def __init__(self, message: str, json_response: dict = None):
        self.status_code: int = 452
        self.message: str = message
        self.json_response: dict = json_response or {}


class BackendException(MagicException):
    pass


class FrontendException(MagicException):
    pass


class FirestoreException(MagicException):
    pass


class TwilioException(MagicException):
    pass


@g.app.exception_handler(MagicException)
def backend_exception_handler(request: Request, exc: MagicException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": f"{exc.message}",
            "json_response": exc.json_response,
        },
    )
