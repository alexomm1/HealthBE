import urllib.parse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from mysite import settings
import requests

def home(request):
    return render(request, 'myapp/index.html')

def tests_view(request):
    return render(request, 'myapp/all_test.html')

class GetJWTTokensView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        refresh = RefreshToken.for_user(request.user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            }
        })


def google_login_redirect(request):
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"

    params = {
        "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        "redirect_uri": "http://127.0.0.1:8000/oauth/callback/google/",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    print(url)
    return redirect(url)


def google_login_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("отсутствует код от гугла", status=400)

    token_data = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        'redirect_uri': 'http://127.0.0.1:8000/oauth/callback/google/',
        'grant_type': 'authorization_code',
    }

    token_res = requests.post('https://oauth2.googleapis.com/token', data=token_data)
    if token_res.status_code != 200:
        return HttpResponse(f"ошибка токена: {token_res.text}", status=400)

    access_token = token_res.json().get('access_token')

    user_res = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        params={'access_token': access_token}
    )
    user_info = user_res.json()
    google_email = user_info.get('email')
    google_name = user_info.get('given_name', 'google_user')

    if not google_email:
        return HttpResponse("нету email", status=400)

    user, created = User.objects.get_or_create(
        email=google_email,
        defaults={'username': google_email.split('@')[0]}
    )

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    refresh = RefreshToken.for_user(user)
    request.session['jwt_access'] = str(refresh.access_token)
    request.session['jwt_refresh'] = str(refresh)

    return redirect('home')



