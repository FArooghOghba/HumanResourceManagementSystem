from typing import Any, Dict

from src.hr_management_system.departments.models import Department, Position


def create_department(*, department_data: Dict[str, Any]) -> 'Department':

    """
    Create a Department instance using the provided data.

    Args:
        department_data (Dict[str, Any]): A dictionary containing the department
            details. Expected keys are:
                - 'code': Unique department code.
                - 'name': Department name.

    Returns:
        Department: The newly created Department object.

    Raises:
        Exception: Propagates any exception raised during the save operation.
    """

    department = Department(
        code=department_data['code'],
        name=department_data['name'],
    )
    department.save()

    return department


def create_position(*, position_data: Dict[str, Any]) -> 'Position':

    department_code = position_data['department_code']
    department = Department.objects.get(code=department_code)

    position = Position(
        title=position_data['title'],
        department=department,
        description=position_data['description'],
    )
    position.save()

    return position
