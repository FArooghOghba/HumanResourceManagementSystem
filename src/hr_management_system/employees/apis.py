from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.hr_management_system.employees.serializers import InputEmployeeSerializer, OutputEmployeeSerializer
from src.hr_management_system.employees.services import create_employee
from src.hr_management_system.employees.selectors import get_employees


class EmployeeDetailAPIView(APIView):

    """
    API View to create an Employee.

    The HR manager provides employee data via the input serializer. 
    The view first creates a user using the user service, then creates an employee.
    """

    input_serializer = InputEmployeeSerializer
    output_serializer = OutputEmployeeSerializer

    @extend_schema(
        request=InputEmployeeSerializer, responses=OutputEmployeeSerializer
    )
    def post(self, request, *args, **kwargs):

        # Validate input data
        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            # Call the employee creation service
            employee = create_employee(employee_data=data)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the created employee using output serializer
        output_serializer = self.output_serializer(employee)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class EmployeeListAPIView(APIView):

    """
    API View to create an Employee.

    The HR manager provides employee data via the input serializer.
    The view first creates a user using the user service, then creates an employee.
    """

    output_serializer = OutputEmployeeSerializer

    @extend_schema(
        responses=OutputEmployeeSerializer
    )
    def get(self, request, *args, **kwargs):

        try:
            employees = get_employees()
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        output_serializer = self.output_serializer(employees, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)
