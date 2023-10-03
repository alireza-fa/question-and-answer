from rest_framework import serializers

from qanda.models import Question, Category


class QuestionCreateSerializer(serializers.ModelSerializer):
    categories = serializers.MultipleChoiceField(choices=Category.get_choices())

    class Meta:
        model = Question
        fields = ('subject', 'body', 'categories')
