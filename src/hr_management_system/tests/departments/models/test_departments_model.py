import pytest
from mongoengine.errors import NotUniqueError, ValidationError

from src.hr_management_system.departments.models import Department


def test_create_department_model_return_successful() -> None:

    """
    Test that a Department instance is created successfully with valid data.

    This test creates a Department instance using a valid uppercase code and checks that:
      - The code and name are correctly assigned.
      - The default headcount is 0.
    """

    test_department = Department(code="HR-001", name="Human Resources")

    assert test_department.code == "HR-001"
    assert test_department.name == "Human Resources"
    assert test_department.headcount == 0
    # assert test_department.manager is None


def test_create_department_model_with_code_lowercase_return_error() -> None:

    """
    Test that creating a Department with a lowercase code raises a ValidationError.

    The department code is required to match a regex for uppercase letters, numbers,
    and hyphens. This test verifies that saving a department with a lowercase code
    triggers a ValidationError.
    """

    # Create a department with a code in lowercase (invalid format).
    test_department = Department(code="hr-001", name="Human Resources")

    with pytest.raises(ValidationError) as err:
        test_department.save()

    assert "String value did not match validation regex" in str(err.value)


def test_create_department_model_with_none_unique_code_return_error(
        first_test_department: 'Department'
) -> None:

    """
    Test that creating a Department with an existing code raises a NotUniqueError.

    This test uses a fixture to obtain an existing department and then attempts to create
    another department with the same code, expecting a NotUniqueError to be raised.

    Args:
        first_test_department (Department): A fixture providing an existing Department instance.
    """

    existed_code = first_test_department.code
    test_department = Department(code=existed_code, name="test name")

    with pytest.raises(NotUniqueError) as err:
        test_department.save()

    assert "Tried to save duplicate unique keys" in str(err.value)


# def test_manager_validation(department_factory, employee_factory):
#     # Assuming you have an EmployeeFactory
#     dept = department_factory()
#     emp = employee_factory(department=dept)
#
#     # Valid manager assignment
#     dept.manager = emp
#     dept.save()
#
#     # Invalid manager (from different department)
#     emp2 = employee_factory()  # Default department
#     dept.manager = emp2
#
#     with pytest.raises(ValidationError) as err:
#         dept.save()
#
#     assert "Manager must belong to this department" in str(err.value)