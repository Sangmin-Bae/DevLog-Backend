from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import SignUpSerializer


class SignUpView(APIView):
    """
    사용자 회원가입 요청을 처리하는 API 뷰
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        회원가입 요청을 검증하고 유저를 생성한 후, 결과 반환
        """
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "message": "User successfully created",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
