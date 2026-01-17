from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserAvatarView, TagViewSet, RecipeViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('users/me/avatar/', UserAvatarView.as_view(), name='user-avatar'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),

]
