import requests
from django.shortcuts import render
from rest_framework import viewsets, permissions
from mysite import settings

def test_result(request):
    token = request.session.get('jwt_access', None)
    print(token)
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{settings.API_BASE_URL}/results/", headers = headers)

    if response.status_code == 200:
        results = response.json()
    else:
        results = []
    return render(request, 'results/results_view.html', {"results": results})
