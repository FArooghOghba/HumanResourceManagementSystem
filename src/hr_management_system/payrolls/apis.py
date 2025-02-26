from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.hr_management_system.payrolls.selectors import get_payrolls
from src.hr_management_system.payrolls.serializers import InputPayrollSerializer, OutputPayrollSerializer
from src.hr_management_system.payrolls.services import create_payroll


class PayrollDetailAPIView(APIView):

    """
    API View to create an Employee.

    The HR manager provides employee data via the input serializer.
    The view first creates a user using the user service, then creates an employee.
    """

    input_serializer = InputPayrollSerializer
    output_serializer = OutputPayrollSerializer

    @extend_schema(
        request=InputPayrollSerializer, responses=OutputPayrollSerializer
    )
    def post(self, request, *args, **kwargs):

        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            payroll = create_payroll(payroll_data=data)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the created employee using output serializer
        output_serializer = self.output_serializer(payroll)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class PayrollListAPIView(APIView):

    """

    """

    output_serializer = OutputPayrollSerializer

    @extend_schema(
        responses=OutputPayrollSerializer
    )
    def get(self, request, *args, **kwargs):

        try:
            payrolls = get_payrolls()
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        output_serializer = self.output_serializer(payrolls, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)
