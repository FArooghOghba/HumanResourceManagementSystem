from rest_framework import serializers

from src.hr_management_system.employees.models import Employee, GenderStatusChoices
from src.hr_management_system.departments.models import Position
from src.hr_management_system.users.serializers import OutputUserSerializer


class InputEmployeeSerializer(serializers.Serializer):

    """
    Serializer for input when creating an Employee.
    """

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    # gender = serializers.ChoiceField(choices=GenderStatusChoices)
    # position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
    employment_start_date = serializers.DateTimeField()
    phone = serializers.CharField()
    birthdate = serializers.DateField()
    father_name = serializers.CharField(max_length=200)
    # For embedded documents, you can either pass a nested dict or handle them separately.
    # military_status = serializers.DictField()
    # degree_status = serializers.DictField()
    # marital_status = serializers.DictField()
    child_number = serializers.IntegerField(default=0)


class OutputEmployeeSerializer(serializers.Serializer):

    """
    Serializer for output representation of an Employee.
    Handles MongoEngine relationships and embedded documents.
    """
    employment_id = serializers.IntegerField(read_only=True)
    user = OutputUserSerializer(read_only=True)
    gender = serializers.CharField(read_only=True)
    employment_start_date = serializers.DateTimeField(read_only=True)
    employment_status = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    birthdate = serializers.DateField(read_only=True)
    father_name = serializers.CharField(read_only=True)
    child_number = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Handle MongoDB ObjectId
        data['id'] = str(instance.id)

        # Add nested user data
        data['user'] = OutputUserSerializer(instance.user).data

        # Add future fields (uncomment when ready)
        # data['position'] = str(instance.position.id) if instance.position else None
        # data['department'] = self._get_department(instance)
        # data.update(self._handle_embedded_docs(instance))

        return data

    # def get_department(self, obj: Employee) -> Any:
    #     """
    #     Returns the department derived from the employee's position.
    #     """
    #     return str(obj.department)
