import requests
from django.shortcuts import render
from rest_framework import viewsets, permissions
from mysite import settings
from tests.models import Results
from tests.serializers import ResultsSerializer
from .models import TestResult
from .serializers import TestResultSerializer

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

class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)