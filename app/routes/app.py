from fastapi import HTTPException, FastAPI, Response, Depends, APIRouter, Query, Form
from uuid import UUID, uuid4
from starlette.responses import RedirectResponse

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from app.schemas.basicverifier import BasicVerifier
from app.models.user import SessionData, User

from app.schemas.helpers import request_to_github, validate_form
from app.schemas.user import serializeDict
from app.config.db import client
from datetime import date
from app.config.settings import settings

# Configure cookie settings for session management
cookie_params = CookieParameters()

# GitHub API credentials
github_client_id = settings.github_client_id
github_client_secret = settings.github_client_secret

# Uses UUID Create a session cookie for session management
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)

# Create an in-memory session backend
backend = InMemoryBackend[UUID, SessionData]()

# Create a session verifier that uses the UUID as identifier
verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

# Create an API router for the user endpoint
user = APIRouter()


@user.get('/')
async def github_login():
    """
    This is the home page, it just shows a message
    """
    return "Welcome to Wolf and Badger app please to login go here: ->  http://0.0.0.0:15400/github-login"


@user.get('/github-login')
async def github_login():
    """
    Redirect the user to the GitHub OAuth authorization page.
    """
    return RedirectResponse(f'{settings.login_url}{github_client_id}', status_code=302)


@user.get('/github-code')
async def github_code(response: Response, code: str = Query(None)):
    """
    Receive code from the GitHub logging and init the session
    """
    # request access token and user profile from GitHub
    profile, access_token = await request_to_github(github_client_id=github_client_id,
                                                    github_client_secret=github_client_secret,
                                                    code=code)
    active_session = False
    if access_token:
        active_session = True

    # create a User object with the profile information
    _user = User(active_session=active_session,
                 account_id=profile.get("id"),
                 account_url=profile.get("html_url"),
                 account_login=profile.get("login"),
                 account_name=profile.get("name"),
                 avatar_url=profile.get("avatar_url"),
                 account_company=profile.get("company"),
                 account_blog=profile.get("blog"),
                 account_location=profile.get("location"),
                 account_bio=profile.get("bio"),
                 account_twitter_username=profile.get("twitter_username"),
                 provider="github")

    # create a session and associated data
    session = uuid4()
    data = SessionData(account_id=profile.get("id"), account_name=profile.get("name"))

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    # check if the user already has a profile, and update or create accordingly
    if client.testingwb.profile.find_one({"account_id": _user.account_id}):
        client.testingwb.profile.update_one(
            {"account_id": _user.account_id},
            {"$set": {"access_token": access_token, "active_session": active_session}}
        )
        return f"Welcome back to Wolf & Badger, nice to see you again {data}"
    else:
        client.testingwb.profile.insert_one(dict(_user))
        return f"Welcome to Wolf & Badger, Thanks for register {data}"


@user.get("/user-profile", dependencies=[Depends(cookie)])
async def user_info(session_data: SessionData = Depends(verifier)):
    """
    get the profile from the user logged
    """
    # extract the user's account id from the session data
    id = session_data.account_id
    # check if the user's profile exists in the database
    if client.testingwb.profile.find_one({"account_id": id}):
        # retrieve and serialize the user's profile data
        data = serializeDict(client.testingwb.profile.find_one({"account_id": id}))
        return f"Here is the info for your user: {data}"
    else:
        return "The user does not exist"


@user.put('/update-user', dependencies=[Depends(cookie)])
async def update_user(name: str = Form(None),
                      company: str = Form(None),
                      blog: str = Form(None),
                      location: str = Form(None),
                      bio: str = Form(None),
                      past_address: str = Form(None),
                      actual_address: str = Form(None),
                      phone_number: str = Form(None),
                      age: int = Form(None),
                      gender: str = Form(None),
                      birthday: date = Form(None),
                      email: str = Form(None),
                      session_data: SessionData = Depends(verifier)):
    """
    This update the parameters passed through the function
    """
    # extract the user's account id from the session data
    id = session_data.account_id

    # validate the form data
    data = await validate_form(name, company, blog, location, bio, past_address,
                               actual_address, phone_number, age, gender, birthday, email)

    # check if the user's profile exists in the database
    if client.testingwb.profile.find_one({"account_id": id}):
        # create a dictionary with the update data
        update_data = {f"{k}": v for k, v in data.items()}
        # update the user's profile
        client.testingwb.profile.update_one({"account_id": id}, {
            "$set": update_data
        })

    if data:
        return "successfully user updated"
    else:
        return "You did not update any parameter"


@user.delete("/delete-profile", dependencies=[Depends(cookie)])
async def delete_user(session_data: SessionData = Depends(verifier)):
    """
    Delete the complete profile of the logged user and then clean the session
    """
    # extract the user's account id from the session data
    id = session_data.account_id
    # delete the user's profile from the database
    client.testingwb.profile.find_one_and_delete({"account_id": id})
    # delete the session
    await backend.delete(session_id)
    # delete the cookie
    cookie.delete_from_response(response)
    return f'Your user: {session_data} was successfully deleted from Wolf & Badger Data base and you are logged Out'


@user.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    """
    Return the session data of the current logged-in user
    """
    return session_data


@user.post("/logout")
async def logout_del_session(response: Response, session_id: UUID = Depends(cookie)):
    """
    Delete the session and the cookie, and log out the user
    """
    # delete the session
    await backend.delete(session_id)
    # delete the cookie
    cookie.delete_from_response(response)
    return "Session finished: You are logged Out!"
