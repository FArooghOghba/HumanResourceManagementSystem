from typing import TYPE_CHECKING

import pytest

from src.hr_management_system.tests.factories.department_factories import (
    DepartmentFactory, PositionFactory
)

if TYPE_CHECKING:
    from src.hr_management_system.departments.models import Department


@pytest.fixture
def first_test_department() -> 'Department':

    """
    Fixture to create and return a test Department instance using DepartmentFactory.

    Returns:
        Department: A Department instance with generated values.
    """

    return DepartmentFactory()

