from rest_framework import viewsets, generics, status
from rest_framework.permissions import (
    IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserAvatarSerializer, TagSerializer, RecipeSerializer)
from djoser.views import UserViewSet as DjoserUserViewSet
from food.models import Tag, Recipe
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        if self.action == 'me':
            return [IsAuthenticated()]
        return super().get_permissions()


class UserAvatarView(generics.UpdateAPIView):
    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'delete']

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.avatar:
            user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
