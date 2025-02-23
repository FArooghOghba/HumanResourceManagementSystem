from typing import TYPE_CHECKING

import pytest
from mongoengine.errors import NotUniqueError, ValidationError

from src.hr_management_system.departments.models import Position

if  TYPE_CHECKING:
    from src.hr_management_system.departments.models import Department


def test_create_position_model_return_successful(
        first_test_department: 'Department'
) -> None:

    """
    Test that a Position instance can be created successfully with valid data.

    This test creates a Position with a valid title and a reference to a Department.
    It asserts that:
      - The title is correctly set.
      - The associated department's code starts with "DEPT-".
      - The position is active by default.

    Args:
        first_test_department (Department): A fixture providing a
        test Department instance.
    """

    test_position = Position(
        title="Senior Engineer", department=first_test_department
    )

    assert test_position.title == "Senior Engineer"
    assert test_position.department.code.startswith("DEPT-")
    assert test_position.is_active is True


def test_create_position_model_department_immutability_return_error(
        first_test_position: 'Position', first_test_department: 'Department',
) -> None:

    """
    Test that attempting to modify the department of an existing Position
    raises a ValidationError.

    This test assumes that once a Position is created, its associated
    department is immutable.
    Changing the department and saving should trigger a ValidationError.

    Args:
        first_test_position (Position): A fixture providing a test
        Position instance.
        first_test_department (Department): A fixture providing a
        test Department instance.
    """

    first_test_position.department = first_test_department

    with pytest.raises(ValidationError) as err:
        first_test_position.save()

    assert "Position department cannot be modified" in str(err.value)


def test_create_position_model_with_existed_title_return_error(
        first_test_position: 'Position'
) -> None:

    """
    Test that creating a Position with a duplicate title in the same
    department raises a NotUniqueError.

    This test first obtains an existing Position's title and department,
    then attempts to create a new Position with the same title and department.
    This should violate the unique index constraint, raising a NotUniqueError.

    Args:
        first_test_position (Position): A fixture providing a test Position instance.
    """

    existed_title = first_test_position.title
    existed_department = first_test_position.department

    test_position = Position(
        title=existed_title,
        department=existed_department
    )

    with pytest.raises(NotUniqueError) as err:
        test_position.save()

    assert "Tried to save duplicate unique keys" in str(err.value)
