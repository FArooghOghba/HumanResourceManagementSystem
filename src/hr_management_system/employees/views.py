from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.hr_management_system.employees.serializers import InputEmployeeSerializer, OutputEmployeeSerializer
from src.hr_management_system.employees.services import create_employee


class EmployeeAPIView(APIView):

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
            employee = create_employee(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                # gender=data['gender'],
                # position=data['position'],
                employment_start_date=data['employment_start_date'],
                phone=data['phone'],
                birthdate=data['birthdate'],
                father_name=data['father_name'],
                # military_status=data['military_status'],
                # degree_status=data['degree_status'],
                # marital_status=data['marital_status'],
                child_number=data.get('child_number', 0)
            )
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the created employee using output serializer
        output_serializer = self.output_serializer(employee)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)
