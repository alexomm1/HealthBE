from django.db.models import Q, Count
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from tests.models import TestAttempts, Test
from tests.serializers import TestSubmissionSerializer, TestAttemptDetailSerializer, TestAttemptSerializer, \
    AttemptHistorySerializer


class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TestSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save_results(user=request.user)
            return Response({"message": "Результаты успешно сохранены!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTestAttemptView(generics.ListAPIView):
    serializer_class = TestAttemptDetailSerializer

    def get_queryset(self):
        return TestAttempts.objects.filter(user=self.request.user)


class TestDetailView(generics.RetrieveAPIView):
    serializer_class = TestAttemptDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestAttempts.objects.filter(user=self.request.user)

class AllAttemptsView(ListAPIView):
    serializer_class = TestAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestAttempts.objects.filter(user=self.request.user)\
            .select_related('test')\
            .prefetch_related('results')

class AttemptHistoryView(ListAPIView):
    serializer_class = AttemptHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Test.objects.annotate(
            attempts_count=Count('attempts', filter=Q(attempts__user=user))
        ).filter(attempts_count__gt=0)
