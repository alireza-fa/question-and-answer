from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class JwtLoginView(APIView):

    def get(request):
        return Response(status=status.HTTP_200_OK)


class JwtRefreshView(APIView):
    pass


class JwtVerifyView(APIView):
    pass
