from typing import Any

from django.core.exceptions import ValidationError
from src.hr_management_system.users.services import create_user_with_generated_credentials
from src.hr_management_system.employees.models import Employee


def create_employee(
        *, email: str, first_name: str, last_name: str,
        employment_start_date, phone: str, birthdate, father_name: str,
        # military_status: str, degree_status: str, marital_status: str,
        child_number: int,

) -> 'Employee':

    """
    Service to create an employee. First, create a user using the user service,
    then create and save an employee instance linking to that user.

    Args:
        email (str): Email address for the user.
        first_name (str): first_name for the user.
        last_name (str): last_name for the user.
        gender (str): Gender, e.g. 'M', 'F', or 'O'.
        position: Position object (or its ID) for the employee.
        employment_start_date: Start date/time of employment.
        phone (str): Employee's phone number.
        birthdate: Birthdate of the employee.
        father_name (str): Name of the employee's father.
        military_status: A MilitaryStatus embedded document instance.
        degree_status: A DegreeStatus embedded document instance.
        marital_status: A MaritalStatus embedded document instance.
        child_number (int): Number of children.

    Returns:
        Employee: The created employee instance.

    Raises:
        ValidationError: If user creation or employee creation fails.
    """

    user = create_user_with_generated_credentials(
        email=email, first_name=first_name, last_name=last_name
    )

    # Create the employee instance
    employee = Employee(
        user=user,
        # gender=gender,
        # position=position,
        employment_start_date=employment_start_date,
        phone=phone,
        birthdate=birthdate,
        father_name=father_name,
        # military_status=military_status,
        # degree_status=degree_status,
        # marital_status=marital_status,
        child_number=child_number,
    )

    employee.save()
    return employee
