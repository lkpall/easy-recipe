from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import CookingStep, Ingredient, Recipe

User = get_user_model()


class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="pinheiro", password="senha123")
        self.recipe = Recipe.objects.create(
            title="Arroz Doce", description="Receita simples", user=self.user
        )

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), "Arroz Doce")

    def test_ingredient_str(self):
        ing = Ingredient.objects.create(
            description="Leite condensado", recipe=self.recipe
        )
        self.assertEqual(str(ing), "Leite condensado")

    def test_cooking_step_str(self):
        step = CookingStep.objects.create(
            instructions="Mexer tudo", order=1, recipe=self.recipe
        )
        self.assertIn("1 - Arroz Doce", str(step))
