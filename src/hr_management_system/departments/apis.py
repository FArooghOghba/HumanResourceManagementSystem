from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.hr_management_system.departments.selectors import get_departments
from src.hr_management_system.departments.serializers import (
    InputDepartmentSerializer, InputPositionSerializer,
    OutputDepartmentSerializer, OutputPositionSerializer
)
from src.hr_management_system.departments.services import create_department, create_position


class DepartmentDetailAPIView(APIView):

    """

    """

    input_serializer = InputDepartmentSerializer
    output_serializer = OutputDepartmentSerializer

    @extend_schema(
        request=InputDepartmentSerializer, responses=OutputDepartmentSerializer
    )
    def post(self, request, *args, **kwargs):

        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            department = create_department(department_data=data)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the created employee using output serializer
        output_serializer = self.output_serializer(department)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class DepartmentListAPIView(APIView):

    """

    """

    output_serializer = OutputDepartmentSerializer

    @extend_schema(
        responses=OutputDepartmentSerializer
    )
    def get(self, request, *args, **kwargs):

        try:
            departments = get_departments()
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        output_serializer = self.output_serializer(departments, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)


class PositionDetailAPIView(APIView):

    """

    """

    input_serializer = InputPositionSerializer
    output_serializer = OutputPositionSerializer

    @extend_schema(
        request=InputPositionSerializer, responses=OutputPositionSerializer
    )
    def post(self, request, *args, **kwargs):

        serializer = self.input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            position = create_position(position_data=data)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the created employee using output serializer
        output_serializer = self.output_serializer(position)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)
