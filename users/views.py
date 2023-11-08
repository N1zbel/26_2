from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import UserLoginSerializer, UserSerializer


class UserLoginViewSet(viewsets.ViewSet):
    """
            Представление для аутентификации пользователя с созданием токена.

            Атрибуты:
                serializer_class : Сериализатор для аутентификации.

            Методы:
                create: Создания токена и возврата данных пользователя вместе с токеном.

            Returns:
                Response: Ответ от сервера с токеном и данными пользователя.
    """
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)

        return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
