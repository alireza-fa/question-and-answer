from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from qanda.serializers import QuestionCreateSerializer
from qanda.cruds import create_question


class CategoryListView(APIView):
    pass


class CategoryQuestionListView(APIView):
    pass


class QuestionListView(APIView):
    pass


class QuestionCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        question = create_question(
            user=request.user,
            subject=vd['subject'],
            body=vd['body'],
            category_ids=vd['categories'])
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AnswerCreateView(APIView):
    pass


class QuestionAnswerListView(APIView):
    pass


class QuestionLineView(APIView):
    pass


class QuestionDislikeView(APIView):
    pass


class AnswerLikeView(APIView):
    pass


class AnswerDislikeView(APIView):
    pass


class QuestionSaveView(APIView):
    pass


class AnswerSaveView(APIView):
    pass
