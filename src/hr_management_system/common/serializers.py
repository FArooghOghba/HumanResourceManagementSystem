from rest_framework import serializers
from mongoengine import fields
from bson import ObjectId


class ObjectIdField(serializers.Field):

    """
    Custom serializer field to handle MongoDB ObjectId.
    Converts ObjectId to string for output and validates/converts string back to ObjectId for input.
    """

    def to_representation(self, value):
        """Convert ObjectId to string."""

        return str(value)

    def to_internal_value(self, data):
        """Convert string to ObjectId, with validation."""
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError('Invalid ObjectId')


class MongoDocumentSerializer(serializers.Serializer):

    """
    Base serializer for MongoEngine documents.

    This serializer provides automatic field mapping between MongoEngine documents
    and DRF serializers. It handles common MongoDB fields (id, created_at, updated_at)
    and supports nested documents, reference fields, and list fields.

    Usage:
        class MyDocumentSerializer(MongoDocumentSerializer):
            class Meta:
                model = MyDocument
                fields = ('id', 'field1', 'field2', ...)
    """

    def __init__(self, *args, **kwargs):

        """
        Initialize the serializer and set up field mapping.
        Only includes fields that are explicitly declared in Meta.fields.
        """

        super().__init__(*args, **kwargs)
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'model'):
            model = self.Meta.model
            declared_fields = getattr(self.Meta, 'fields', None)

            # Only add these fields if they're explicitly declared in Meta.fields
            if 'id' in declared_fields:
                self.fields['id'] = ObjectIdField(read_only=True)
            if 'created_at' in declared_fields:
                self.fields['created_at'] = serializers.DateTimeField(read_only=True)
            if 'updated_at' in declared_fields:
                self.fields['updated_at'] = serializers.DateTimeField(read_only=True)

            # Add other model fields
            for field_name in declared_fields:
                if field_name not in ['id', 'created_at', 'updated_at'] and field_name not in self.fields:
                    model_field = model._fields.get(field_name)
                    if model_field:
                        self.fields[field_name] = self._create_field_for_mongo_type(model_field)

    def _create_field_for_mongo_type(self, model_field):

        """
        Map MongoEngine field types to DRF serializer fields.

        Args:
            model_field: MongoEngine field instance

        Returns:
            DRF serializer field instance
        """

        # Map MongoEngine field types to DRF serializer fields
        field_mapping = {
            fields.StringField: serializers.CharField,
            fields.IntField: serializers.IntegerField,
            fields.FloatField: serializers.FloatField,
            fields.BooleanField: serializers.BooleanField,
            fields.DateTimeField: serializers.DateTimeField,
            fields.ReferenceField: self._get_reference_serializer,
            fields.ListField: self._get_list_serializer,
            fields.DictField: serializers.DictField,
        }

        field_class = field_mapping.get(type(model_field), serializers.CharField)

        # Handle special cases for reference and list fields
        if field_class == self._get_reference_serializer:
            return field_class(model_field)
        elif field_class == self._get_list_serializer:
            return field_class(model_field)

        # Set up field kwargs (e.g., required)
        field_kwargs = {}
        if hasattr(model_field, 'required'):
            field_kwargs['required'] = model_field.required

        return field_class(**field_kwargs)

    def _get_reference_serializer(self, model_field):

        """
        Create a serializer for referenced documents (foreign key relationships).

        Args:
            model_field: MongoEngine ReferenceField instance

        Returns:
            Serializer instance for the referenced document
        """

        # Handle ReferenceField by creating a nested serializer
        referenced_model = model_field.document_type

        class DynamicDocumentSerializer(MongoDocumentSerializer):
            class Meta:
                model = referenced_model

        return DynamicDocumentSerializer()

    def _get_list_serializer(self, model_field):

        """
        Create a serializer for list fields.

        Args:
            model_field: MongoEngine ListField instance

        Returns:
            ListField serializer with appropriate child serializer
        """

        # Handle ListField by creating a list serializer
        field = self._create_field_for_mongo_type(model_field.field)
        return serializers.ListField(child=field)

    def create(self, validated_data):

        """Create a new document instance."""

        model_class = self.Meta.model
        instance = model_class(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):

        """Update an existing document instance."""

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance