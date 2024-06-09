from rest_framework import serializers
from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
    """
    Serializer class for NewsArticle model.

    This serializer handles the serialization and deserialization of NewsArticle objects,
    converting between model instances and JSON representations. It specifies the fields
    to be included in the serialized output.

    Attributes:
        model (type): The model class that this serializer serializes.
        fields (list): The list of fields to be included in the serialized output.
    """

    class Meta:
        model = NewsArticle
        fields = ["title", "url"]
