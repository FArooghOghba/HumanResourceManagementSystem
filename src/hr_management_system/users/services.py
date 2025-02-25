import string
from random import choices

from django_mongoengine.mongo_auth.managers import get_user_document


User = get_user_document()


def generate_username(first_name: str, last_name: str, length: int = 4) -> str:

    """
    Generate a unique username by combining the first name, last name, and a random string.

    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        length (int): The length of the random suffix. Defaults to 4.

    Returns:
        str: The generated username.
    """

    random_suffix = ''.join(choices(string.ascii_lowercase + string.digits, k=length))
    return f"{first_name.lower()}.{last_name.lower()}{random_suffix}"


def generate_password(length: int = 12) -> str:

    """
    Generate a random password.

    Args:
        length (int): Length of the password. Defaults to 12.

    Returns:
        str: The generated password.
    """

    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choices(characters, k=length))


def create_user_with_generated_credentials(
        *, email: str, first_name: str, last_name: str,
        **extra_fields
) -> tuple[User, str, str]:

    """
    Create a user with generated credentials (username and password).

    The generated credentials can be emailed to the employee later.

    Args:
        email (str): Email address for the new user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        extra_fields: Additional keyword arguments for the user creation.

    Returns:
        tuple[BaseUser, str, str]: A tuple containing the created user instance,
                                    the generated username, and the generated password.

    Raises:
        ValueError: If required fields are missing.
    """

    # Generate a unique username based on first and last names.
    username = generate_username(first_name, last_name)

    # Generate a secure random password.
    password = generate_password()

    # Create the user via your custom user manager/service.
    user = User.create_user(
        email=email,
        username=username,
        password=password,
        **extra_fields
    )

    user.first_name = first_name
    user.last_name = last_name
    user.save()

    # Here, you could trigger an email sending function to notify the employee of their credentials.
    # For example: send_credentials_email(email, username, password)

    return user
