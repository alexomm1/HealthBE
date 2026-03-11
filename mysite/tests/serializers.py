from django.db.models import Sum
from rest_framework import serializers
from tests.models import TestResults, TestAttempts, Test

#save
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

    def create(self, validated_data):
        user = self.context['request'].user

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

#получение результатов

class FactorStatsSerializer(serializers.Serializer):
    factor_id = serializers.IntegerField()
    factor_name = serializers.CharField()
    avg_score = serializers.FloatField()
    max_score = serializers.IntegerField()
    attempts_count = serializers.IntegerField()

class AttemptDetailWithFactorSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = TestAttempts
        fields = ('id', 'completed_at', 'total_score', 'results')

    def get_results(self, obj):
        return [
            {
                'factor_id': r.factor_id, 'score': r.score
            } for r in obj.results.all()
        ]

    def get_total_score(self, obj):
        return obj.results.aggregate(Sum('score'))['score__sum'] or 0


# #all down get
# class TestResultReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TestResults
#         fields = ['factor_id', 'score']
#
# class TestAttemptDetailSerializer(serializers.ModelSerializer):
#     results = TestResultReadSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = TestAttempts
#         fields = ['id', 'test_id', 'user', 'completed_at', 'results']
#
#     def get_results(self, obj):
#         results = obj.user.results.all()
#         return  TestResultReadSerializer(results, many=True).data
#
# class TestAttemptSerializer(serializers.ModelSerializer):
#     tests = serializers.CharField(source='test.title', read_only=True)
#     score = serializers.SerializerMethodField()
#     class Meta:
#         model = TestAttempts
#         fields = ['id', 'tests', 'score', 'completed_at']
#
#     def get_score(self, obj):
#         results = obj.results.all()
#
#         count = results.count()
#         if count == 0:
#             return 0
#         else:
#             return results.aggregate(Sum('score'))['score__sum']
#
# class AttemptHistorySerializer(serializers.ModelSerializer):
#     attempts_count = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = Test
#         fields = ['id', 'title', 'attempts_count']
#
#
# #получение результатов тестирований
# class AttemptSerializer(serializers.ModelSerializer):
#     results = FactorResultSerializer(many=True, read_only=True)
#     class Meta:
#         model = TestAttempts
#         fields = ['id', 'test', 'completed_at', 'results']
#
# class TestSerializer(serializers.ModelSerializer):
#     attempts = AttemptSerializer(many=True, read_only=True)
#     class Meta:
#         model = Test
#         fields = ['id', 'title', 'description', 'attempts']
#
#
# #new ser
# class FactorStatsSerializer(serializers.Serializer):
#     factor_id = serializers.IntegerField()
#     factor_name = serializers.CharField()
#     avg_score = serializers.FloatField()
#     max_score = serializers.IntegerField()
#     attempts_count = serializers.IntegerField()
#
# class ComplexTestSerializer(serializers.ModelSerializer):
#     attempts_count = serializers.IntegerField()
#     avg_score = serializers.FloatField()
#     best_score = serializers.IntegerField()
#     factor_stats = FactorStatsSerializer(many=True, read_only=True)
#     recent_attempts = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Test
#         fields = ['id', 'title', 'description', 'attempts_count', 'avg_score', 'best_score', 'factor_stats']
#
#     def get_recent_attempts(self, obj):
#         attempts = obj.attempts.filter(user=self.context['user']).order_by('-completed_at')[:5]
#
#         return AttemptDetailWithFactorSerializer(attempts, many=True).data