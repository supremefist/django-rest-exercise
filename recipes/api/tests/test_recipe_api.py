from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.serializers import RecipeSerializer
from core.models import Recipe, Ingredient

RECIPES_URL = reverse("api:recipes-list")


def detail_url(recipe_id):
    """Return recipe detail URL

    :param recipe_id:
    :return:
    """
    return reverse("api:recipe-detail", args=[recipe_id])


def sample_recipe(name, **params):
    """Helper function to create recipes

    :param name:
    :return:
    """
    ingredients = params.pop("ingredients", None)
    recipe = Recipe.objects.create(name=name, **params)
    if ingredients:
        for name in ingredients:
            recipe.ingredients.add(Ingredient.objects.create(name=name))

    return recipe


class RecipeAPITests(TestCase):
    """None

    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_basic_recipe_list(self):
        """Test retrieving recipes

        :return:
        """
        sample_recipe(name="Bolognaise")

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-name")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(serializer.data, res.data)

    def test_create_basic_recipe(self):
        """Test creating recipes

        :return:
        """
        payload = {
            "name": "Bolognaise",
            "description": "Put it in the oven",
            "ingredients": [
                {"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEquals(status.HTTP_201_CREATED, res.status_code)
        recipe = Recipe.objects.get(name=payload["name"])
        serializer = RecipeSerializer(recipe, many=False)

        self.assertEqual(serializer.data, res.data)

    def test_create_basic_recipe_no_ingredients(self):
        """Test creating recipe with no ingredients specified

        :return:
        """
        payload = {
            "name": "Bolognaise",
            "description": "Put it in the oven",
        }

        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEquals(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_recipe_list_view(self):
        """Test list view on list of recipes

        :return:
        """
        sample_recipe(
            "Omelette", description="Delicious", ingredients=["Eggs", "Bacon"])
        sample_recipe(
            "Bread", description="Dry", ingredients=["Eggs", "Flour"])

        recipes = Recipe.objects.all().order_by("-name")

        res = self.client.get(RECIPES_URL)

        self.assertEquals(status.HTTP_200_OK, res.status_code)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(serializer.data, res.data)

    def test_recipe_list_view_with_filter(self):
        """Test list view on list of recipes with filter

        :return:
        """
        sample_recipe(
            "Omelette", description="Delicious", ingredients=["Eggs", "Bacon"])
        sample_recipe(
            "Bread", description="Dry", ingredients=["Eggs", "Flour"])

        recipes = Recipe.objects.filter(name="Delicious")

        res = self.client.get(RECIPES_URL, {
            "name": "Deli"
        })

        self.assertEquals(status.HTTP_200_OK, res.status_code)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(serializer.data, res.data)

    def test_recipe_detail_view(self):
        """Test detail view on created recipe

        :return:
        """
        recipe = sample_recipe(
            "Omelette", description="Delicious", ingredients=["Eggs", "Bacon"])

        url = detail_url(recipe.id)
        res = self.client.get(url)

        self.assertEquals(status.HTTP_200_OK, res.status_code)
        serializer = RecipeSerializer(recipe, many=False)
        self.assertEqual(serializer.data, res.data)

    def test_update_recipe(self):
        """Test can update recipe

        :return:
        """
        recipe = sample_recipe(
            "Omelette", description="Delicious", ingredients=["Eggs", "Bacon"])

        self.assertEquals(2, Ingredient.objects.all().count())

        patched_data = {
            "name": "Omlete",
            "description": "Extra delicious",
            "ingredients": [{"name": "Peppers"}]
        }

        url = detail_url(recipe.id)
        res = self.client.patch(url, patched_data, format="json")

        self.assertEquals(status.HTTP_200_OK, res.status_code)

        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe, many=False)
        self.assertEqual(serializer.data, res.data)

        self.assertEquals(1, recipe.ingredients.count())
        self.assertEquals(1, Ingredient.objects.all().count())

    def test_partially_patch_recipe(self):
        """Test can partially patch recipe

        :return:
        """
        recipe = sample_recipe(
            "Omelette", description="Delicious", ingredients=["Eggs", "Bacon"])

        patched_data = {
            "name": "Omlete",
        }

        url = detail_url(recipe.id)
        res = self.client.patch(url, patched_data, format="json")

        self.assertEquals(status.HTTP_200_OK, res.status_code)

        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe, many=False)
        self.assertEqual(serializer.data, res.data)

        self.assertEquals(2, recipe.ingredients.count())
        self.assertEquals(patched_data["name"], recipe.name)
        self.assertEquals("Delicious", recipe.description)

    def test_delete_recipe(self):
        """Test can delete recipe

        :return:
        """
        recipe = sample_recipe(
            "Omelette", description="Delicious", ingredients=["Eggs", "Bacon"])

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEquals(status.HTTP_204_NO_CONTENT, res.status_code)

        self.assertEquals(0, Ingredient.objects.all().count())
        self.assertEquals(0, Recipe.objects.all().count())
