from rest_framework import serializers
from tests.models import Test, Question, AnswerOption, Factor, Results


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerOptionSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


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
