from rest_framework import serializers


class OutputUserSerializer(serializers.Serializer):

    """
    Serializer for output representation of a user.
    Handles MongoEngine User document serialization.
    """
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert MongoEngine ObjectId to string
        data['id'] = str(instance.id)
        return data
