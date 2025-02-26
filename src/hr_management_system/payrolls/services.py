from typing import Any, Dict

from src.hr_management_system.employees.selectors import get_employee
from src.hr_management_system.payrolls.models import Payroll


INSURANCE = 500
TAX = 1_500


def create_payroll(*, payroll_data: Dict[str, Any]) -> 'Payroll':
    employee = get_employee(employee_id=payroll_data['employee_id'])

    payroll = Payroll(
        employee=employee,
        base_salary=payroll_data['base_salary'],
        insurance=INSURANCE,
        tax=TAX
    )
    payroll.save()

    return payroll