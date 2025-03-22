from rest_framework import serializers

from src.hr_management_system.common.serializers import MongoDocumentSerializer
from src.hr_management_system.departments.models import Department, Position


class InputDepartmentSerializer(serializers.Serializer):

    """
    Serializer for handling department creation and update requests.
    
    This serializer validates and processes input data when creating or updating
    a Department document in MongoDB.
    
    Fields:
        code (str): Unique department identifier code, limited to 10 characters
        name (str): Human-readable department name, limited to 100 characters
    
    Example:
        {
            "code": "HR001",
            "name": "Human Resources"
        }
    """

    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)


class OutputDepartmentSerializer(MongoDocumentSerializer):

    """
    Serializer for department response data.
    
    This serializer handles the conversion of Department documents to JSON responses.
    It inherits from MongoDocumentSerializer to handle MongoDB-specific field types.
    
    Fields:
        id (ObjectId): MongoDB document identifier
        created_at (datetime): Timestamp of department creation
        code (str): Department unique identifier code
        name (str): Department name
        headcount (int): Current number of employees in the department
    
    Example:
        {
            "id": "507f1f77bcf86cd799439011",
            "code": "HR001",
            "name": "Human Resources",
            "headcount": 25
        }
    """

    class Meta:
        model = Department
        fields = ('id', 'created_at', 'code', 'name', 'headcount')


class InputPositionSerializer(serializers.Serializer):

    """
    Serializer for handling position creation and update requests.
    
    This serializer validates and processes input data when creating or updating
    a Position document in MongoDB.
    
    Fields:
        title (str): Job title/position name, limited to 100 characters
        department_code (str): Reference to department code, limited to 10 characters
        description (str): Detailed position description, limited to 512 characters
    
    Example:
        {
            "title": "Senior Software Engineer",
            "department_code": "ENG001",
            "description": "Lead developer position responsible for..."
        }
    """

    title = serializers.CharField(max_length=100)
    department_code = serializers.CharField(max_length=10)
    description = serializers.CharField(max_length=512)


class OutputPositionSerializer(MongoDocumentSerializer):

    """
    Serializer for position response data.
    
    This serializer handles the conversion of Position documents to JSON responses.
    It includes a nested department representation through OutputDepartmentSerializer.
    
    Fields:
        id (ObjectId): MongoDB document identifier
        created_at (datetime): Timestamp of position creation
        title (str): Position title
        description (str): Position description
        is_active (bool): Position status
        department (dict): Nested department information
    
    Example:
        {
            "id": "507f1f77bcf86cd799439012",
            "title": "Senior Software Engineer",
            "description": "Lead developer position...",
            "is_active": true,
            "department": {
                "id": "507f1f77bcf86cd799439011",
                "code": "ENG001",
                "name": "Engineering"
            }
        }
    """

    department = OutputDepartmentSerializer

    class Meta:
        model = Position
        fields = ('id', 'created_at', 'title', 'description', 'is_active')
