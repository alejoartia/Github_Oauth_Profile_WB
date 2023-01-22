import httpx
from app.config.settings import settings


async def request_to_github(github_client_id, github_client_secret, code):
    """
    Send a request to GitHub API to get an access token and user profile.
    """
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as Requestclient:
        res = await Requestclient.post(url=f'{settings.token_url}', params=params,
                                       headers=headers)
    response_json = res.json()
    access_token = response_json['access_token']
    headers.update({'Authorization': f'Bearer {access_token}'})

    async with httpx.AsyncClient() as Requestclient:
        res = await Requestclient.get(url=f'{settings.user_url}', headers=headers)
        profile = res.json()

    return profile, access_token


async def validate_form(name, company, blog, location, bio, past_address, actual_address, phone_number, age, gender,
                        birthday, email):
    """
    Validate form data and return a dictionary with the valid data.
    """

    data = {}

    if isinstance(name, str):
        data['account_name'] = name
    if isinstance(company, str):
        data['account_company'] = company
    if isinstance(blog, str):
        data['account_blog'] = blog
    if isinstance(location, str):
        data['account_location'] = location
    if isinstance(bio, str):
        data['account_bio'] = bio
    if isinstance(past_address, str):
        data['user_past_address'] = past_address
    if isinstance(actual_address, str):
        data['user_actual_address'] = actual_address
    if isinstance(phone_number, str):
        data['user_phone_number'] = phone_number
    if isinstance(age, int) and age > 0:
        data['user_age'] = age
    if isinstance(gender, str):
        data['user_gender'] = gender
    if isinstance(birthday, str):
        data['user_birthday'] = birthday
    if isinstance(email, str):
        data['user_email'] = email

    return data
