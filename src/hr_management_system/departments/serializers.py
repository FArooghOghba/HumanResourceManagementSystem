from rest_framework import serializers


class InputDepartmentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)


class OutputDepartmentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    headcount = serializers.IntegerField()
