from rest_framework import viewsets, permissions
from tests.models import Test
from tests.serializers import TestSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
