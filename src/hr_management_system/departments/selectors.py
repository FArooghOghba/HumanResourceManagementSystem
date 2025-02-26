from typing import Optional

from django_mongoengine import QuerySet

from src.hr_management_system.departments.models import Department


def get_departments() -> Optional[QuerySet['Department']]:

    """

    """

    departments = Department.objects()
    return departments
