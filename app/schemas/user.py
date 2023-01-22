def userEntity(item) -> dict:
    """
    Convert a single user item from the database to a dictionary with specific keys.
    """
    return {
        "id": str(item["_id"]),
        "active_session": item["active_session"],
        "account_id": item["account_id"],
        "account_url": item["account_url"],
        "account_login": item["account_login"],
        "account_name": item["account_name"],
        "avatar_url": item["avatar_url"],
        "account_company": item["account_company"],
        "account_blog": item["account_blog"],
        "account_location": item["account_location"],
        "account_bio": item["account_bio"],
        "account_twitter_username": item["account_twitter_username"],
        "provider": item["provider"],
    }


def usersEntity(entity) -> list:
    """
    Convert a list of user items from the database to a list of dictionaries with specific keys.
    """
    return [userEntity(item) for item in entity]


def serializeDict(a) -> dict:
    """
    Convert ObjectId to string and return a serialized dictionary.
    """
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    """
    Convert ObjectId to string and return a list of serialized dictionaries
    """
    return [serializeDict(a) for a in entity]
