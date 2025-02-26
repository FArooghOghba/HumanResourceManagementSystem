from typing import Optional

from django_mongoengine import QuerySet

from src.hr_management_system.payrolls.models import Payroll


def get_payrolls() -> Optional[QuerySet['Payroll']]:

    """

    """

    payrolls = Payroll.objects()
    return payrolls
