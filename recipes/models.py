from django.contrib.auth import get_user_model
from django.db import models

CURRENT_USER = get_user_model()


class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        CURRENT_USER, on_delete=models.CASCADE, related_name="recipes"
    )

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )

    def __str__(self) -> str:
        return self.description


class CookingStep(models.Model):
    step_id = models.AutoField(primary_key=True)
    instructions = models.TextField()
    order = models.PositiveIntegerField()
    recipe = models.ForeignKey(
        Recipe,
        related_name="steps",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "order"], name="unique_step_order_per_recipe"
            )
        ]

    def __str__(self) -> str:
        return f"{self.order} - {self.recipe.title}"
