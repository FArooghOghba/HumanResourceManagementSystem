from typing import Optional

from django_mongoengine.mongo_auth.managers import get_user_document

from src.hr_management_system.core.exceptions import (
    UserNotActiveError, UserNotVerifiedError
)
from src.hr_management_system.employees.models import Employee


User = get_user_document()


def get_employees() -> Optional['Employee']:

    """

    """


    return Employee.objects()