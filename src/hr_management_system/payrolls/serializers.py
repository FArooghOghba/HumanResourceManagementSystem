from rest_framework import serializers

from src.hr_management_system.employees.serializers import OutputEmployeeSerializer


class InputPayrollSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    base_salary = serializers.DecimalField(max_digits=10, decimal_places=2)


class OutputPayrollSerializer(serializers.Serializer):
    employee = OutputEmployeeSerializer()
    base_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    insurance = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_salary = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # def create(self, validated_data):
    #     # Convert employee from string id to Employee document if needed
    #     employee_id = validated_data.pop('employee')
    #     from src.hr_management_system.employees.models import Employee
    #     employee_obj = Employee.objects.get(pk=employee_id)
    #     payroll = Payroll(employee=employee_obj, **validated_data)
    #     payroll.save()
    #     return payroll

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['net_salary'] = instance.net_salary
        return representation
