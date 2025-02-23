from mongoengine import CASCADE, NULLIFY
from mongoengine import fields
from mongoengine.errors import ValidationError

from src.hr_management_system.common.models import BaseModel


class Department(BaseModel):

    """
    Department model representing an organizational unit.

    Attributes:
        code (str): Unique department code (e.g., 'HR-IT'). Must be uppercase,
        alphanumeric with hyphens.
        name (str): Full department name (e.g., 'Human Resources').
        headcount (int): Current number of active employees in the department.
    """

    code = fields.StringField(
        max_length=10,
        unique=True,
        required=True,
        regex=r'^[A-Z0-9\-]+$',  # Uppercase alphanumeric
        help_text="Unique department code (e.g., HR-IT)",
        error_messages={
            'unique': "Department code already exists",
            'regex': "Only uppercase letters, numbers and hyphens allowed"
        }
    )

    name = fields.StringField(
        max_length=100,
        required=True,
        unique=True,
        help_text="Full department name (e.g., Human Resources)",
        error_messages={'unique': "Department name must be unique"}
    )

    # manager = fields.ReferenceField(
    #     document_type='employees.Employee',
    #     reverse_delete_rule=NULLIFY,
    #     help_text="Must be an active employee in this department"
    # )

    headcount = fields.IntField(
        default=0,
        min_value=0,
        help_text="Current number of active employees"
    )

    meta = {
        'collection': 'departments',
        'indexes': [
            {'fields': ['code'], 'unique': True},
            {'fields': ['name'], 'unique': True},
            # {'fields': ['manager']},
            {'fields': ['headcount']}
        ],
        'ordering': ['code'],
    }

    def clean(self) -> None:

        """
        Custom clean method for additional validation.

        This method currently calls the superclass clean() method.
        You may add custom validations (e.g., for the manager field) here.

        Raises:
            ValidationError: If any custom validation fails.
        """

        super().clean()

        # Manager validation
        # if self.manager:
        #     if self.manager.department != self:
        #         raise ValidationError("Manager must belong to this department")
        #     if not self.manager.is_active:
        #         raise ValidationError("Manager must be an active employee")


    def __str__(self) -> str:

        """
        Returns a string representation of the department.

        Returns:
            str: The department's code and name.
        """

        return f"{self.code} - {self.name}"


class Position(BaseModel):

    """
    Position model representing a job role within a department.

    Attributes:
        title (str): Official position title (e.g., 'Senior Software Engineer').
        department (Department): Reference to the associated Department.
        description (str): Optional description of the position.
        is_active (bool): Indicates whether the position is active.
    """

    title = fields.StringField(
        max_length=100,
        required=True,
        help_text="Official position title (e.g., Senior Software Engineer)",
        error_messages={'required': "Position title is mandatory"}
    )
    department = fields.ReferenceField(Department, reverse_delete_rule=CASCADE)
    description = fields.StringField()
    is_active = fields.BooleanField(default=True)

    meta = {
        'collection': 'positions',
        'indexes': [
            {'fields': ['title', 'department'], 'unique': True},
            {'fields': ['department']},
            {'fields': ['is_active']}
        ]
    }

    def clean(self) -> None:

        """
        Custom clean method to enforce immutability of the department field.

        If the Position already exists in the database, changing its department
        is not allowed and will raise a ValidationError.

        Raises:
            ValidationError: If the department field is modified after creation.
        """

        super().clean()

        if self.pk:  # Only for existing instances
            original = Position.objects.get(id=self.pk)  # Get DB version
            if self.department != original.department:  # Compare values
                raise ValidationError('Position department cannot be modified')

    def __str__(self) -> str:

        """
        Returns a string representation of the position.

        Returns:
            str: The position's title followed by its department code.
        """

        return f"{self.title} ({self.department.code})"
