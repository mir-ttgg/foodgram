from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    UserAvatarView, UserViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('users/me/avatar/', UserAvatarView.as_view(), name='user-avatar'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),

]
