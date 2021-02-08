from rest_framework import viewsets

from api import serializers
from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in database

    """
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Filter queryset appropriately

        :return:
        """
        queryset = self.queryset

        name_filter = self.request.query_params.get("name", None)
        if name_filter:
            queryset = queryset.filter(name__startswith=name_filter)

        queryset = queryset.order_by("-name")

        return queryset

    def perform_create(self, serializer):
        """Create a new recipe

        :param serializer:
        :return:
        """
        serializer.save()

    def get_serializer_class(self):
        """Return appropriate serializer class

        :return:
        """
        return self.serializer_class
