from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_mongoengine.mongo_auth.models import AbstractUser
from mongoengine import fields

from src.hr_management_system.common.models import BaseModel


class BaseUser(AbstractUser, BaseModel):

    """
    Custom User Model that uses MongoEngine's Document combined with common fields from BaseModel.
    Inherits from django_mongoengine.mongo_auth.models.AbstractUser for authentication support.

    Attributes:
        username (str): The user's username. Must match a specific regex pattern.
        is_verified (bool): Flag indicating whether the user is verified.
        USERNAME_FIELD (str): Field used for authentication (email).
        REQUIRED_FIELDS (list[str]): List of required fields for user creation.
    """

    username = fields.StringField(
        max_length=150,
        regex=r'^[\w.@+-]+$',  # Similar to UnicodeUsernameValidator
        verbose_name=_("username"),
        help_text=_("Required. 150 characters or fewer. Letters, numbers and @/./+/-/_ characters"),
        required=True,
    )

    is_verified = fields.BooleanField(default=False)

    # These attributes help with Django integration.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    @classmethod
    def _create_user(
            cls, username: str, password: str, email: str | None = None,
            create_superuser: bool = False
    ) -> "BaseUser":

        """
        Create and save a new user with the provided username, password, and email.

        Args:
            username (str): The desired username.
            password (str): The desired password.
            email (Optional[str]): The user's email address. Must be provided.
            create_superuser (bool): If True, creates a superuser with elevated privileges.

        Returns:
            BaseUser: The created and saved user instance.

        Raises:
            ValueError: If email is not provided or username is empty.
        """

        now = timezone.now()

        # Normalize the address by lowercasing the domain part of the email
        # address.
        if email is not None:
            try:
                email_name, domain_part = email.strip().split("@", 1)
            except ValueError:
                pass
            else:
                email = "@".join([email_name.lower(), domain_part.lower()])
        else:
            raise ValueError("Users must have an email address")

        if not username:
            raise ValueError('The username must be set.')

        user = cls(username=username, email=email, date_joined=now)
        user.set_password(password)

        # Set superuser flags if requested.
        if create_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.is_verified = True
        user.save()

        return user

    meta = {
        'indexes': [
            {'fields': ['email'], 'unique': True},
        ],
        'app_label': 'users',  # Ensures Django registers this model under the 'users' app
    }

    def __str__(self) -> str:

        """
        Return the string representation of the user.

        Returns:
            str: The user's email.
        """

        return self.email
