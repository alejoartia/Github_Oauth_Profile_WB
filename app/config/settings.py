from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """
    Returns all the .env variables in a pydantic model to be use in all the classes
    """
    env: str = Field("prod", env="ENV")
    login_url: str = Field("https://github.com/login/oauth/authorize?client_id=", env="LOGIN_URL")
    token_url: str = Field("https://github.com/login/oauth/access_token", env="TOKEN_URL")
    user_url: str = Field("https://api.github.com/user", env="USER_URL")
    github_client_id: str = Field("dd78be3c4b01dfe4e534", env="GITHUB_CLIENT_ID")
    github_client_secret: str = Field("eba0c67512ca9087cc1e602736762544868c0738", env="GITHUB_CLIENT_SECRET")
    mongo_db_connectio_string: str = Field(
        "mongodb+srv://wolfandbadger:adminpass@wolfandbadger.z7uhqro.mongodb.net/?retryWrites=true&w=majority",
        env="MONGO_DB_CONNECTION_STRING "
    )

    class Config:
        env_file = '.env'


settings = Settings()


