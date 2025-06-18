from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers.cooking_step import CookingStepSerializer
from recipes.serializers.ingredient import IngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    steps = CookingStepSerializer(many=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Recipe
        exclude = ("user",)
        read_only_fields = ("recipe_id", "created_at", "updated_at")

    def create(self, validated_data) -> Recipe:
        ingredients_data = validated_data.pop("ingredients")
        steps_data = validated_data.pop("steps")
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_data:
            recipe.ingredients.create(**ingredient, recipe=recipe)

        for step in steps_data:
            recipe.steps.create(**step, recipe=recipe)

        return recipe

    def update(self, instance, validated_data) -> Recipe:
        ingredients_data = validated_data.pop("ingredients", None)
        steps_data = validated_data.pop("steps", None)
        instance = super().update(instance, validated_data)

        if ingredients_data:
            instance.ingredients.all().delete()

            for ingredient in ingredients_data:
                instance.ingredients.create(**ingredient, recipe=instance)

        if steps_data:
            instance.steps.all().delete()

            for step in steps_data:
                instance.steps.create(**step, recipe=instance)

        return instance
