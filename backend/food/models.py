from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150, verbose_name='Имя пользователя')
    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия пользователя')
    username = models.CharField(
        max_length=150, verbose_name='Юзернейм', unique=True)
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    password = models.CharField(verbose_name='Пароль')
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=50)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=32, unique=True)


class Recipe(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название рецепта')
    author = models.ForeignKey(
        User, related_name='recipes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField('Описание')
    ingredients = ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes'

    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='used_in_recipes')
    quantity = models.FloatField('количество', default=1.0)
    unit = models.CharField('единица', max_length=20,
                            default='г')

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient}"


class Favorite(models.Model):
    """Модель для избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'recipe')
        ordering = ['-id']


class ShoppingCart(models.Model):
    """Модель для списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ('user', 'recipe')
        ordering = ['-id']
