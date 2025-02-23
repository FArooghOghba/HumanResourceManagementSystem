import pytest
from django_mongoengine.mongo_auth.managers import get_user_document
from mongoengine.errors import NotUniqueError, ValidationError


User = get_user_document()


def test_create_user_with_email_return_successful() -> None:

    """
    Test that creating a user with valid email, username, and password is successful.

    Asserts:
        - The user's email is stored correctly.
        - Default flags (is_staff, is_superuser, is_verified) are False.
        - The password is hashed and verified.
        - Only one user exists with the given email.
    """

    email = 'test@example.com'
    username = 'test_user'
    password = 'test_pass123'
    test_user = User.create_user(
        email=email,
        username=username,
        password=password
    )

    assert test_user.email == email
    assert test_user.is_staff is False
    assert test_user.is_superuser is False
    assert test_user.is_verified is False
    assert test_user.check_password(password) is True
    assert User.objects.filter(email=email).count() == 1

@pytest.mark.parametrize(
    'email, username, email_expected_format',
    [
        ('test1@EXAMPLE.com', 'test_username1', 'test1@example.com'),
        ('Test2@Example.com', 'test_username2', 'test2@example.com'),
        ('TEST3@EXAMPLE.com', 'test_username3', 'test3@example.com'),
        ('test4@example.COM', 'test_username4', 'test4@example.com'),
    ],
)
def test_create_user_normalized_email_return_successful(
        email: str, username: str, email_expected_format: str
) -> None:

    """"
    Test that the email address is normalized upon user creation.

    Args:
        email (str): The input email with mixed case.
        username (str): The username for the new user.
        email_expected_format (str): The expected normalized email.

    Asserts:
        - The stored email is normalized to lowercase.
    """

    test_user = User.create_user(
        email=email, username=username, password='sample123'
    )

    assert test_user.email == email_expected_format


@pytest.mark.parametrize(
    'wrong_email',
    [
        '@EXAMPLE.com',
        'Test2@',
        'TEST3',
        '',
    ],
)
def test_create_user_with_wrong_email_raises_error(wrong_email: str) -> None:

    """
    Test that creating a user with an invalid email format raises a ValidationError.

    Args:
        wrong_email (str): The invalid email input.

    Asserts:
        - A ValidationError is raised when the email format is invalid.
    """

    with pytest.raises(ValidationError):
        User.create_user(
            email=wrong_email, username='test_user123', password='test123'
        )


def test_create_user_without_username_raises_error() -> None:

    """
    Test that creating a user without a username raises a ValueError.

    Asserts:
        - A ValueError is raised if the username is empty.
    """

    with pytest.raises(ValueError):
        User.create_user(
            email='test@example.com', username='', password='test123'
        )


def test_create_user_with_existed_email_return_error(first_test_user: 'User') -> None:

    """
    Test that creating a user with an already existing email raises
    a NotUniqueError.

    Asserts:
        - A NotUniqueError is raised when attempting to create a
        duplicate user with the same email.
    """

    existed_email = first_test_user.email

    with pytest.raises(NotUniqueError):
        User.create_user(
            email=existed_email,
            username='first_test_user',
            password='test'
        )



def test_create_user_with_existed_username_return_error(first_test_user: 'User') -> None:

    """
    Test that creating a user with an already existing username
    raises a NotUniqueError.

    Asserts:
        - A NotUniqueError is raised when attempting to create
        a duplicate user with the same username.
    """

    existed_username = first_test_user.username

    with pytest.raises(NotUniqueError):
        User.create_user(
            email='test2@example.com',
            username=existed_username,
            password='test'
        )


def test_create_superuser_return_successful() -> None:

    """
    Test that creating a superuser is successful and sets appropriate flags.

    Asserts:
        - The superuser has is_verified, is_staff, and is_superuser set to True.
    """

    email = 'test@example.com'
    username = 'test_user'
    password = 'test_pass123'
    user = User.create_superuser(
        email=email,
        username=username,
        password=password
    )

    assert user.is_verified is True
    assert user.is_staff is True
    assert user.is_superuser is True
