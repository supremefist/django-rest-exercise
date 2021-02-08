from rest_framework import serializers
from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient objects

    """

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe objects

    """
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients:
            Ingredient.objects.get_or_create(recipe=recipe, **ingredient_data)

        return recipe

    def update(self, instance, validated_data):
        """Update a recipe

        :param instance:
        :param validated_data:
        :return:
        """
        ingredients = validated_data.pop("ingredients", None)

        recipe = super().update(instance, validated_data)

        if ingredients:
            for ingredient in recipe.ingredients.all():
                ingredient.delete()

            for ingredient_data in ingredients:
                ingredient = Ingredient.objects.create(
                    name=ingredient_data["name"])
                recipe.ingredients.add(ingredient)

        recipe.save()

        return recipe
