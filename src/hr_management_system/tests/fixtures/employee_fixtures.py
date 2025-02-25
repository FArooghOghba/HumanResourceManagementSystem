from typing import Dict, TYPE_CHECKING

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


@pytest.fixture
def first_test_employee_payload() -> Dict[str, str]:

    """
    Fixture for creating a test employee instance.

    This fixture uses the `EmployeeFactory` factory
    to create a test employee instance. The created employee
    can be used in tests to simulate a employee with predefined
    attributes for testing various scenarios.

    :return: a dict test employee payload
    """

    return EmployeeFactory.create_payload()
