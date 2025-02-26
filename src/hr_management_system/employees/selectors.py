from typing import Optional

from django_mongoengine import QuerySet
from django_mongoengine.mongo_auth.managers import get_user_document

from src.hr_management_system.core.exceptions import (
    UserNotActiveError, UserNotVerifiedError
)
from src.hr_management_system.employees.models import Employee


def get_employee(*, employee_id: int) -> Optional['Employee']:

    """

    """
    try:
        return Employee.objects.get(employment_id=employee_id)
    except Employee.DoesNotExist:
        return None


def get_employees() -> Optional[QuerySet['Employee']]:

    """

    """

    return Employee.objects()