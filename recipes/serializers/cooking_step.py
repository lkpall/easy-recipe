from rest_framework import serializers

from recipes.models import CookingStep


class CookingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingStep
        fields = ("instructions", "order")
