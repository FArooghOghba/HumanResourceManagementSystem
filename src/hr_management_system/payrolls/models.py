from decimal import Decimal

from mongoengine import fields

from src.hr_management_system.common.models import BaseModel
from src.hr_management_system.employees.models import Employee


class Payroll(BaseModel):
    # Link payroll record to an employee
    employee = fields.ReferenceField(Employee, required=True, unique=True)

    base_salary = fields.DecimalField(required=True, precision=2, min_value=Decimal('0.00'))
    insurance = fields.DecimalField(required=True, precision=2, min_value=Decimal('0.00'))
    tax = fields.DecimalField(required=True, precision=2, min_value=Decimal('0.00'))

    meta = {
        'collection': 'payroll'
    }

    @property
    def gross_salary(self) -> Decimal:
        """Calculate the gross salary."""
        return self.base_salary * 30

    @property
    def net_salary(self) -> Decimal:
        """Calculate the net salary."""
        return self.gross_salary - self.insurance - self.tax

    def clean(self):
        if self.net_salary < Decimal('0.00'):
            raise ValueError("Net salary cannot be negative.")

    def __str__(self) -> str:

        """
        Returns a string representation of the payroll.
        """
        return f"{self.employee} -> {self.net_salary}"
