from typing import Any, Dict

from src.hr_management_system.departments.models import Department, Position


def create_department(*, department_data: Dict[str, Any]) -> 'Department':

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
