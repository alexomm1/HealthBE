from django.db.models import Sum
from rest_framework import serializers
from tests.models import TestResults, TestAttempts, Test
from tests.service import create_test_submission


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
        return create_test_submission(
            user=self.context['request'].user,
            test_id=validated_data['test_id'],
            results_data=validated_data['results']
        )

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
