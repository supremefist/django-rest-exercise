"""All django models required for recipe app

"""
from django.db import models

MAX_NAME_LENGTH = 256


class Recipe(models.Model):
    """Model representing a recipe

    """
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.CharField(max_length=1024)


class Ingredient(models.Model):
    """Model representing an ingredient

    """
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    recipe = models.ForeignKey(
        'Recipe', on_delete=models.CASCADE, related_name="ingredients",
        null=True)
