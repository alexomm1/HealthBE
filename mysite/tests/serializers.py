from rest_framework import serializers
<<<<<<< feature/86c83t13e-save-test-result
from tests.models import TestResults, TestAttempts
=======
from tests.models import Test, Question, AnswerOption, Factor, Results
>>>>>>> develop

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

<<<<<<< feature/86c83t13e-save-test-result
    class Meta:
        model = TestAttempts
        fields = ['id', 'test_id', 'user', 'completed_at', 'results']

    def get_results(self, obj):
        results = obj.user.results.all()
        return  TestResultReadSerializer(results, many=True).data
=======

class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = ['id', 'name', 'test']

class TestSerializer(serializers.ModelSerializer):
    questions = FactorSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'questions']

class ResultsSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source="factor.test.title", read_only=True)
    factor_name = serializers.CharField(source="factor.name", read_only=True)
    class Meta:
        model = Results
        fields = ['id', 'test_title', 'factor_name', 'user', 'score']
>>>>>>> develop
