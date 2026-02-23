from django.db.models import Sum
from rest_framework import serializers
from tests.models import TestResults, TestAttempts, Test


class FactorResultSerializer(serializers.Serializer):
    factor_id = serializers.IntegerField()
    score = serializers.IntegerField()

    def validate_score(self, score):
        if score < 0:
            raise serializers.ValidationError('Результат не должен быть меньше 0!')
        return score

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

class TestAttemptSerializer(serializers.ModelSerializer):
    tests = serializers.CharField(source='test.title', read_only=True)
    score = serializers.SerializerMethodField()
    class Meta:
        model = TestAttempts
        fields = ['id', 'tests', 'score', 'completed_at']

    def get_score(self, obj):
        results = obj.results.all()

        count = results.count()
        if count == 0:
            return 0
        else:
            return results.aggregate(Sum('score'))['score__sum']


class AttemptHistorySerializer(serializers.ModelSerializer):
    attempts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'attempts_count']