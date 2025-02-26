from typing import Optional

from django_mongoengine import QuerySet

from src.hr_management_system.departments.models import Department, Position


def get_departments() -> Optional[QuerySet['Department']]:

    """

    """

    departments = Department.objects()
    return departments


def get_positions() -> Optional[QuerySet['Position']]:

    """

    """

    positions = Position.objects()
    return positions
