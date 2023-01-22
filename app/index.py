from fastapi import FastAPI
from app.routes.app import user
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Include the user router in the application
app.include_router(user)

# Add session middleware to the application with a secret key and no maximum age.
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)

# Allow all origins for CORS
origins = ["*"]

# Add CORS middleware to the application with the allowed origins, allow credentials,
# methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
