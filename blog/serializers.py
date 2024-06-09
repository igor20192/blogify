from pyexpat import model
from attr import field
from rest_framework import serializers
from .models import Article, Subscriber


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


class SubscriberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscriber model.

    This serializer is used to convert the Subscriber model instances to and from
    JSON format, enabling the representation and manipulation of subscriber data
    through API requests.

    Attributes:
        Meta (class): Inner class that defines the metadata for the serializer.
            model (Model): Specifies the model class that the serializer is based on.
            fields (list[str]): List of model fields that should be included in the
                                serialized representation. In this case, only the
                                'chat_id' field is included.
    """

    class Meta:
        model = Subscriber
        fields = ["chat_id"]
