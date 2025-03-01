from rest_framework import serializers
from mongoengine import fields as me_fields  # Renamed to avoid conflict


class MongoModelSerializer(serializers.Serializer):

    """
    A base serializer that dynamically maps fields from a MongoEngine model.
    This mimics DRF's ModelSerializer but without needing django-rest-framework-mongoengine.
    """

    def __init__(self, instance=None, data=None, **kwargs):
        if instance is not None and not isinstance(instance, self.Meta.model):
            raise TypeError(f"Expected instance of {self.Meta.model.__name__}, got {type(instance).__name__}")
        super().__init__(data=data, **kwargs)

    @classmethod
    def get_fields(cls) -> dict:

        """
        Dynamically generates serializer fields from the MongoEngine model fields.

        Returns:
            dict: A mapping of field names to serializer fields.
        """

        model = cls.Meta.model
        serializer_fields = {}

        for field_name, model_field in model._fields.items():
            if isinstance(model_field, (me_fields.StringField, me_fields.EmailField)):
                serializer_fields[field_name] = serializers.CharField()
            elif isinstance(model_field, me_fields.IntField):
                serializer_fields[field_name] = serializers.IntegerField()
            elif isinstance(model_field, me_fields.BooleanField):
                serializer_fields[field_name] = serializers.BooleanField()
            elif isinstance(model_field, me_fields.DateTimeField):
                serializer_fields[field_name] = serializers.DateTimeField()
            elif isinstance(model_field, me_fields.ReferenceField):
                # For related objects, represent as a primary key.
                serializer_fields[field_name] = serializers.PrimaryKeyRelatedField(read_only=True)
            else:
                # Fallback: use CharField for unknown field types
                serializer_fields[field_name] = serializers.CharField()

        return serializer_fields

    def to_representation(self, instance) -> dict:

        """
        Convert a model instance into a dictionary of primitive data types.

        Args:
            instance: The MongoEngine model instance.

        Returns:
            dict: A dictionary representation of the instance.
        """

        data = {}
        for field_name, serializer_field in self.get_fields().items():
            # Use getattr to fetch field value; if not found, use None.
            data[field_name] = getattr(instance, field_name, None)
        return data
