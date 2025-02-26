from typing import Any, Dict

from django.core.exceptions import ValidationError

from src.hr_management_system.departments.models import Position
from src.hr_management_system.users.services import create_user_with_generated_credentials
from src.hr_management_system.employees.models import Employee


def create_employee(*, employee_data: Dict[str, Any]) -> 'Employee':

    """
    Service to create an employee. First, create a user using the user service,
    then create and save an employee instance linking to that user.
    Returns:
        Employee: The created employee instance.

    Raises:
        ValidationError: If user creation or employee creation fails.
    """

    email = employee_data['email']
    first_name = employee_data['first_name']
    last_name = employee_data['last_name']

    user = create_user_with_generated_credentials(
        email=email, first_name=first_name, last_name=last_name
    )

    position_title = employee_data['position_title']
    position = Position.objects.get(title=position_title)

    # Create the employee instance
    employee = Employee(
        user=user,
        # gender=gender,
        position=position,
        employment_start_date=employee_data['employment_start_date'],
        phone=employee_data['phone'],
        birthdate=employee_data['birthdate'],
        father_name=employee_data['father_name'],
        # military_status=military_status,
        # degree_status=degree_status,
        # marital_status=marital_status,
        child_number=employee_data.get('child_number', 0),
    )
    employee.save()

    position.department.headcount += 1
    position.save()

    return employee
