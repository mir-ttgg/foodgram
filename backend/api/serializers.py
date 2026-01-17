import re

from django.contrib.auth import get_user_model
from djoser.serializers import \
    UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from food.models import Follow, Ingredient, Recipe, Tag

User = get_user_model()


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ['avatar']


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        return Follow.objects.filter(
            follower=request.user,
            following=obj
        ).exists()

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'password',
                  'is_subscribed', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        allow_empty=False
    )
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        allow_empty=False
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'tags', 'author',
                  'ingredients', 'image', 'text', 'cooking_time']

    def validate_ingredients(self, value):
        """Проверка ингредиентов на существование и корректность"""
        if not value:
            raise serializers.ValidationError(
                "Ингредиенты не могут быть пустыми")

        ingredients_list = []
        for item in value:

            if 'id' not in item or 'amount' not in item:
                raise serializers.ValidationError(
                    "Каждый ингредиент должен содержать id и amount")

            if not Ingredient.objects.filter(id=item['id']).exists():
                raise serializers.ValidationError(
                    f"Ингредиент с id {item['id']} не существует")
            if item['id'] in ingredients_list:
                raise serializers.ValidationError(
                    "Ингредиенты не должны повторяться")
            ingredients_list.append(item['id'])

            # 4. Проверка количества
            if int(item['amount']) < 1:
                raise serializers.ValidationError(
                    "Количество должно быть больше 0")

        return value

    def to_representation(self, instance):
        """
        Подменяем вывод: на вход принимаем ID, а на выход отдаем полные объекты
        """
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(
            instance.tags.all(), many=True).data
        representation['ingredients'] = IngredientSerializer(
            instance.recipe_ingredients.all(), many=True
        ).data
        return representation

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        if ingredients is not None:
            instance.recipe_ingredients.all().delete()
            self.create_ingredients(instance, ingredients)

        return instance

    def create_ingredients(self, recipe, ingredients_data):

        recipe_ingredients_objs = []
        for item in ingredients_data:
            recipe_ingredients_objs.append(
                Ingredient(
                    recipe=recipe,
                    ingredient_id=item['id'],
                    quantity=item['amount']
                )
            )
        Ingredient.objects.bulk_create(recipe_ingredients_objs)


class SubscriptionSerializer(DjoserUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        fields = DjoserUserSerializer.Meta.fields + \
            ('recipes', 'recipes_count', 'is_subscribed')

    def get_is_subscribed(self, obj):

        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        queryset = obj.recipes.all()
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass
        return RecipeShortSerializer(queryset, many=True).data


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']


class UserRegistrationSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'password']

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                'Некорректный формат имени пользователя')


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
