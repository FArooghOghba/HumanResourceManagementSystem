from typing import Any, Dict

from src.hr_management_system.departments.models import Department


def create_department(*, department_data: Dict[str, Any]) -> 'Department':

    department = Department(
        code=department_data['code'],
        name=department_data['name'],
    )
    department.save()

    return department