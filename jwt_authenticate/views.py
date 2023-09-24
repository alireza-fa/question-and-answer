from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from jwt_authenticate.serializers import JwtLoginSerializer, JwtRefreshSerializer, JwtVerifySerializer
from jwt_authenticate.services import user_login


class JwtLoginView(APIView):
    serializer_class = JwtLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        token = user_login(**serializer.validated_data)
        return Response(data=token, status=status.HTTP_200_OK)


class JwtRefreshView(APIView):
    serializer_class = JwtRefreshSerializer

    def post(self, request):
        pass


class JwtVerifyView(APIView):
    serializer_class = JwtVerifySerializer

    def post(self, request):
        pass
