from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from food.models import Ingredient, Recipe, RecipeIngredient, Tag, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Админка для пользователей.
    Позволяет:
    - Менять пароль (стандартный функционал UserAdmin)
    - Блокировать (через галочку is_active)
    - Искать по email и username
    """
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name',
        'is_active',
        'is_staff'
    )
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    """
    Позволяет добавлять ингредиенты прямо на странице рецепта.
    """
    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorites_count')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author__username')
    inlines = (RecipeIngredientInline,)
    empty_value_display = '-пусто-'

    @admin.display(description='В избранном')
    def favorites_count(self, obj):
        return obj.in_favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


admin.site.unregister(Group)

admin.site.site_header = "Администрирование Foodgram"
admin.site.site_title = "Foodgram Admin"
admin.site.index_title = "Добро пожаловать в панель управления"
