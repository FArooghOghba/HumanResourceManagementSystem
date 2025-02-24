from typing import TYPE_CHECKING

import pytest

from src.hr_management_system.tests.factories.employee_factories import EmployeeFactory

if TYPE_CHECKING:
    from src.hr_management_system.employees.models import Employee


@pytest.fixture
def first_test_employee() -> "Employee":
    """Fixture to create a test Employee instance linked to a position."""
    return EmployeeFactory()


@pytest.fixture
def second_test_employee() -> "Employee":
    """Fixture to create a test Employee instance linked to a position."""
    return EmployeeFactory()
