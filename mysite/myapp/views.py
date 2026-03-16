import urllib.parse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from myapp.service import google_auth
from mysite import settings
import requests
from users.models import User


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

    try:
        user = google_auth(code=code)
    except Exception as e:
        return HttpResponse(str(e), status=400)

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    refresh = RefreshToken.for_user(user)
    request.session['jwt_access'] = str(refresh.access_token)
    request.session['jwt_refresh'] = str(refresh)

    return redirect('home')

