from app.models.user import SessionData
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    """
    A basic verifier for sessions.
    """
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        """
        Initialize the BasicVerifier with the given parameters.
        """
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        """
        Get the identifier of the verifier.
        """
        return self._identifier

    @property
    def backend(self):
        """
        Get the backend of the verifier.
        """
        return self._backend

    @property
    def auto_error(self):
        """
        Get the auto_error of the verifier.
        """
        return self._auto_error

    @property
    def auth_http_exception(self):
        """
        Get the auth_http_exception of the verifier.
        """
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """
        Get the auth_http_exception of the verifier.
        """
        return True
