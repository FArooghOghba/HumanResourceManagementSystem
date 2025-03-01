from rest_framework import serializers

from src.hr_management_system.common.serializers import MongoModelSerializer
from src.hr_management_system.departments.models import Department


class InputDepartmentSerializer(serializers.Serializer):

    """
    Serializer for input data when creating or updating a Department.
    """

    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)


class OutputDepartmentSerializer(MongoModelSerializer):

    """
    Serializer for output representation of a Department.
    """

    class Meta:
        model = Department


class InputPositionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    department_code = serializers.CharField(max_length=10)
    description = serializers.CharField(max_length=512)


class OutputPositionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    department_code = OutputDepartmentSerializer
    description = serializers.CharField(max_length=512)
    is_active = serializers.BooleanField()
