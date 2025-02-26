from rest_framework import serializers


class InputDepartmentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)


class OutputDepartmentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    headcount = serializers.IntegerField()


class InputPositionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    department_code = serializers.CharField(max_length=10)
    description = serializers.CharField(max_length=512)


class OutputPositionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    department_code = OutputDepartmentSerializer
    description = serializers.CharField(max_length=512)
    is_active = serializers.BooleanField()
