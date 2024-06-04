from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """A serialiser for the Article model.

    Attributes:
    - model: The model to be serialised.
    - fields: The fields of the model that should be included in the serialised data.
    - read_only_fields: Fields that should be read-only.

    Methods:
    - create: Creates a new Article object using the provided validated data."""

    class Meta:
        model = Article
        fields = ["id", "title", "content", "published_date", "author"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        """Creates a new Article object using the provided validated data.

        Parameters:
        - validated_data: A dictionary of validated data that should be used to create an Article object.

        Returns:
        - A new Article object."""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
