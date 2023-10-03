from typing import List

from django.contrib.auth import get_user_model

from qanda.models import Category, Question


User = get_user_model()


def set_question_categories(question: Question, category_ids: List) -> Question:
    return question.categories.set(Category.objects.filter(id__in=category_ids))


def get_slug(value):
    return value.replace(' ', '-')


def create_question(user: User, subject: str, body: str, category_ids: List) -> Question:
    question = Question.objects.create(
        user=user,
        subject=subject,
        slug=get_slug(value=subject),
        body=body,
    )
    return set_question_categories(question=question, category_ids=category_ids)
