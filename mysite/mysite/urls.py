from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenRefreshView
from myapp.views import GetJWTTokensView, google_login_callback, google_login_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('myapp.urls')),
    path('', include('results.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('logout/', csrf_exempt(LogoutView.as_view(next_page='/')), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get-jwt/', GetJWTTokensView.as_view(), name='get_jwt'),
    path('login/google/', google_login_redirect, name='google_login'),
    path('oauth/callback/google/', google_login_callback, name='google_callback'),
]
