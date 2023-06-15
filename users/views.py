from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from users.models import User
from users.permissions import CustomIsAuthenticated
from .permissions import UserAccessPermission
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from users.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserView(APIView):
    def get(self, request: Request) -> Response:
        accounts = User.objects.all()

        serializer = UserSerializer(accounts, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UserAccessPermission]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        if not request.user.is_employee and user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        if not request.user.is_employee and user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)