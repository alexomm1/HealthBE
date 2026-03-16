from mysite import settings
import requests
from users.models import User


def google_auth(*, code):
    token_data = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        'redirect_uri': 'http://127.0.0.1:8000/oauth/callback/google/',
        'grant_type': 'authorization_code',
    }

    token_res = requests.post('https://oauth2.googleapis.com/token', data=token_data)

    if not token_res.ok:
        raise Exception(f"Google token error: {token_res.text}")

    access_token = token_res.json().get('access_token')

    user_res = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        params={'access_token': access_token}
    )
    user_info = user_res.json()
    email = user_info.get('email')

    if not email:
        raise Exception(f"Отсутствует email")

    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': email.split('@')[0]}
    )

    return user