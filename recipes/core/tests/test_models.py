# from unittest.mock import patch

from django.test import TestCase

from core.models import Recipe, Ingredient


class ModelTests(TestCase):
    """None

    """

    def test_create_recipe_no_ingredients(self):
        """Test creating a new recipe with a name and no ingredients

        :return:
        """
        recipe_name = "Bolognaise"
        Recipe.objects.create(name=recipe_name)

        extracted_recipe = Recipe.objects.get(name=recipe_name)
        self.assertEquals(recipe_name, extracted_recipe.name)

    def test_create_recipe_with_ingredients(self):
        """Test creating a new recipe with a name and some ingredients

        :return:
        """
        recipe_name = "Bolognaise"
        new_recipe = Recipe.objects.create(name=recipe_name)
        new_recipe.ingredients.add(
            Ingredient.objects.create(name="Beef mince"))
        new_recipe.ingredients.add(
            Ingredient.objects.create(name="Spaghetti"))

        extracted_recipe = Recipe.objects.get(name=recipe_name)
        self.assertEquals(2, extracted_recipe.ingredients.count())
