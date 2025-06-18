from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from recipes.models import CookingStep, Ingredient, Recipe

User = get_user_model()


class RecipeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Marina", password="senha123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.url = reverse("recipe-list")

        self.rec = Recipe.objects.create(
            title="Torta", description="de maçã", user=self.user
        )
        Ingredient.objects.create(description="Maçã", recipe=self.rec)
        CookingStep.objects.create(instructions="Cortar maçã", order=1, recipe=self.rec)

    def tearDown(self):
        CookingStep.objects.all().delete()
        Ingredient.objects.all().delete()
        Recipe.objects.all().delete()

    def test_create_recipe(self):
        data = {
            "title": "Pudim",
            "description": "Com leite condensado",
            "ingredients": [{"description": "Leite condensado"}],
            "steps": [
                {"instructions": "Bater tudo", "order": 1},
                {"instructions": "Levar ao forno", "order": 2},
            ],
        }
        response = self.client.post(self.url, data, format="json")

        recipe = Recipe.objects.get(recipe_id=response.data["recipe_id"])

        # assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(recipe.title, "Pudim")
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe.ingredients.first().description, "Leite condensado")
        self.assertEqual(recipe.steps.count(), 2)
        self.assertEqual(recipe.steps.first().instructions, "Bater tudo")

    def test_get_recipes(self):
        response = self.client.get(self.url)
        expected_response = {
            "recipe_id": self.rec.recipe_id,
            "ingredients": [{"description": "Maçã"}],
            "steps": [{"instructions": "Cortar maçã", "order": 1}],
            "title": "Torta",
            "description": "de maçã",
            "username": self.user.username,
        }

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

        for key, value in expected_response.items():
            self.assertEqual(response.data[0][key], value)

    def test_get_recipe_by_id(self):
        response = self.client.get(reverse("recipe-detail", args=[self.rec.recipe_id]))
        expected_response = {
            "recipe_id": self.rec.recipe_id,
            "ingredients": [{"description": "Maçã"}],
            "steps": [{"instructions": "Cortar maçã", "order": 1}],
            "title": "Torta",
            "description": "de maçã",
            "username": self.user.username,
        }

        # assertions
        self.assertEqual(response.status_code, 200)
        for key, value in expected_response.items():
            self.assertEqual(response.data[key], value)

    def test_update_recipe(self):
        data = {
            "title": "Bolo de cenoura",
            "description": "Com cobertura de chocolate",
            "ingredients": [{"description": "Cenoura"}],
            "steps": [{"instructions": "Ralar cenoura", "order": 1}],
        }

        response = self.client.put(
            reverse("recipe-detail", args=[self.rec.recipe_id]), data, format="json"
        )

        # assertions
        self.assertEqual(response.status_code, 200)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

    def test_partial_update_recipe(self):
        data = {
            "title": "Bolo de cenoura e chocolate",
            "description": "Com recheio de morango",
        }

        response = self.client.patch(
            reverse("recipe-detail", args=[self.rec.recipe_id]), data, format="json"
        )

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])

    def test_delete_recipe(self):
        response = self.client.delete(
            reverse("recipe-detail", args=[self.rec.recipe_id])
        )

        # assertions
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Recipe.objects.filter(recipe_id=self.rec.recipe_id).exists())
