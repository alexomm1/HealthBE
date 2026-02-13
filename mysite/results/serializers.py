from rest_framework import serializers
from results.models import TestResult


class TestResultSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source="test.title", read_only=True)
    class Meta:
        model = TestResult
        fields = ['id', 'test', 'test_title', 'score', 'created_at']
        read_only_fields = ['user', 'created_at']