import graphene

from graphene_django.types import DjangoObjectType

from .models import Questions, Answers


class QuestionType(DjangoObjectType):
    class Meta:
        model = Questions


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answers


class Query(object):
    all_questions = graphene.List(QuestionType)
    all_answers = graphene.List(AnswerType)

    def resolve_all_questions(self, info, **kwargs):
        return Questions.objects.all()

    def resolve_all_answers(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Answers.objects.select_related('question').all()