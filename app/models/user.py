from pydantic import BaseModel
from fastapi import FastAPI, Form
from datetime import date


class SessionData(BaseModel):
    """
    Data model for session data.
    """
    account_id: str
    account_name: str


class User(BaseModel):
    """
    Data model for user data.
    """
    account_id: str = None
    account_url: str = None
    account_login: str = None
    account_name: str = None
    avatar_url: str = None
    account_company: str = None
    account_blog: str = None
    account_location: str = None
    account_bio: str = None
    account_twitter_username: str = None
    provider: str = None



