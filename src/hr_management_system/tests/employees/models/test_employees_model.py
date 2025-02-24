import pytest
from datetime import timedelta
from django.utils import timezone
from mongoengine.errors import ValidationError, NotUniqueError

from src.hr_management_system.employees.models import Employee, EmploymentStatusChoices


def test_create_employee_model_return_successful(first_test_employee) -> None:

    """
    Test that a valid Employee instance is created successfully.

    Asserts that:
      - The employment_id is set.
      - The employment_status is 'Active'.
      - The derived department property returns the correct department.
    """

    employee = first_test_employee
    # Assert that the employee has been assigned an employment_id by the SequenceField.
    assert employee.employment_id >= 1000
    assert employee.employment_status == EmploymentStatusChoices.ACTIVE

    # Verify the derived department property returns the same as employee.position.department
    assert employee.department == employee.position.department


def test_create_employee_model_with_wrong_employment_end_date_return_error(
        first_test_employee: 'Employee'
) -> None:

    """
    Test that setting an employment end date earlier than the start date raises a ValidationError.
    """

    employee = first_test_employee
    employee.employment_end_date = employee.employment_start_date - timedelta(days=1)

    with pytest.raises(ValidationError) as err:
        employee.clean()  # Manually call clean() to trigger validation

    assert "Employment end date cannot be before start date" in str(err.value)


def test_create_employee_with_wrong_birthdate_return_error(
        first_test_employee: 'Employee'
) -> None:

    """
    Test that setting a birthdate in the future raises a ValidationError.
    """

    employee = first_test_employee
    employee.birthdate = timezone.now().date() + timedelta(days=1)

    with pytest.raises(ValidationError) as err:
        employee.clean()

    assert "Birthdate cannot be in the future" in str(err.value)


def test_create_employee_with_wrong_uniqueness_of_phone_return_error(
        first_test_employee: 'Employee', second_test_employee: 'Employee'
) -> None:

    """
    Test that creating two employees with the same phone number raises a NotUniqueError.
    """

    existed_phone_number = first_test_employee.phone
    second_test_employee.phone = existed_phone_number

    # Create a second employee with the same phone number.
    with pytest.raises(NotUniqueError):
        second_test_employee.save()


# def test_unique_constraints(employee_factory, user_factory):
#     # Create initial employee
#     user = user_factory.create()
#     emp1 = employee_factory.create(user=user, phone="+1234567890")
#
#     # Test user uniqueness
#     with pytest.raises(ValidationError):
#         employee_factory.create(user=user)
#
#     # Test phone uniqueness
#     with pytest.raises(ValidationError):
#         employee_factory.create(phone="+1234567890")
#
#
#
# def test_position_department_integrity(employee_factory, department_factory, position_factory):
#     # Create position in specific department
#     dept = department_factory.create()
#     position = position_factory.create(department=dept)
#
#     # Valid case
#     emp = employee_factory.create(position=position)
#     assert emp.department == dept
#
#     # Invalid department change
#     new_dept = department_factory.create()
#     position.department = new_dept
#     position.save()
#
#     # Refresh employee and validate
#     emp.refresh_from_db()
#     with pytest.raises(ValidationError):
#         emp.clean()
#
#
# def test_embedded_document_validation(employee_factory):
#     # Test invalid military status
#     with pytest.raises(ValidationError):
#         employee_factory(
#             military_status__status='invalid_status'
#         ).save()
#
#     # Test marital status document requirement
#     with pytest.raises(ValidationError):
#         employee_factory(
#             marital_status__document=None
#         ).save()
#
#
# def test_military_document_storage(employee_factory):
#     emp = employee_factory(
#         military_status__document=b"PDF_CONTENT"
#     )
#     assert emp.military_status.document == b"PDF_CONTENT"