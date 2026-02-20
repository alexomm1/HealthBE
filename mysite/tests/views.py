from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from tests.models import TestAttempts
from tests.serializers import TestSubmissionSerializer, TestAttemptDetailSerializer


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