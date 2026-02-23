from rest_framework import serializers
from tests.models import TestResults, TestAttempts

class FactorResultSerializer(serializers.Serializer):
    factor_id = serializers.IntegerField()
    score = serializers.IntegerField()

    def validate_score(self, score):
        if score < 0:
            raise serializers.ValidationError('Результат не должен быть меньше 0!')

class TestSubmissionSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    results = FactorResultSerializer(many=True)

    def save_results(self, user):
        test_id = self.validated_data['test_id']
        results = self.validated_data['results']

        attempt = TestAttempts.objects.create(user=user, test_id=test_id)

        results_obj = [
            TestResults(
                user = user,
                attempt=attempt,
                factor_id = res['factor_id'],
                score = res['score']
            ) for res in results
        ]

        TestResults.objects.bulk_create(results_obj)

        return attempt


class TestResultReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResults
        fields = ['factor_id', 'score']

class TestAttemptDetailSerializer(serializers.ModelSerializer):
    results = TestResultReadSerializer(many=True, read_only=True)

    class Meta:
        model = TestAttempts
        fields = ['id', 'test_id', 'user', 'completed_at', 'results']

    def get_results(self, obj):
        results = obj.user.results.all()
        return  TestResultReadSerializer(results, many=True).data