from enum import Enum
from typing import Optional

from django.utils import timezone
from mongoengine import DENY, EmbeddedDocument
from mongoengine import fields
from mongoengine.connection import get_db
from mongoengine.errors import ValidationError

from src.hr_management_system.common.models import BaseModel
from src.hr_management_system.departments.models import Department


class MilitaryStatus(EmbeddedDocument):

    """
    Embedded document representing military status.

    Attributes:
        status (StatusChoices): The military status of the employee.
        document: An optional file for supporting documentation.
    """

    class StatusChoices(Enum):
        EXEMPT = 'Exempt'
        COMPLETED = 'Completed'
        POSTPONED = 'Postponed'

    status = fields.EnumField(enum=StatusChoices, required=True)
    document = fields.FileField()


class MaritalStatus(EmbeddedDocument):

    """
    Embedded document representing marital status.

    Attributes:
        status (StatusChoices): The marital status.
        document: An optional file for supporting documentation.
    """

    class StatusChoices(Enum):
        SINGLE = 'Single'
        MARRIED = 'Married'
        DIVORCED = 'Divorced'

    status = fields.EnumField(enum=StatusChoices, required=True)
    document = fields.FileField()


class DegreeStatus(EmbeddedDocument):
    class StatusChoices(Enum):
        BACHELOR = 'Bachelor'
        MASTER = 'Master'
        DOCTORATE = 'Doctorate'
        OTHER = 'Other'

    status = fields.EnumField(enum=StatusChoices, required=True)
    document = fields.FileField()


class GenderStatusChoices(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class EmploymentStatusChoices(Enum):
    ACTIVE = 'Active'
    ON_LEAVE = 'On Leave'
    TERMINATED = 'Terminated'


class Employee(BaseModel):

    """
    Employee model representing an employee in the HR management system.

    Attributes:
        employment_id (int): A unique identifier for the employee.
        user: Reference to the associated user profile (BaseUser).
        gender (GenderStatusChoices): Gender of the employee.
        position: Reference to the employee's job position.
        employment_start_date (datetime): When employment started.
        employment_end_date (datetime): When employment ended (if applicable).
        employment_status (EmploymentStatusChoices): Current employment status.
        phone (str): Contact phone number in full international format.
        birthdate (date): Birthdate of the employee.
        father_name (str): Name of the employee's father.
        military_status (MilitaryStatus): Embedded military status information.
        degree_status (DegreeStatus): Embedded educational degree status.
        marital_status (MaritalStatus): Embedded marital status information.
        child_number (int): Number of children.
    """

    employment_id = fields.IntField(unique=True, required=True)
    user = fields.ReferenceField(
        document_type='users.BaseUser', required=True, unique=True, reverse_delete_rule=DENY
    )
    # gender = fields.EnumField(
    #     enum=GenderStatusChoices,
    #     required=True
    # )
    position = fields.ReferenceField(document_type='departments.Position', reverse_delete_rule=DENY)
    employment_start_date = fields.DateTimeField(default=timezone.now, required=True)
    employment_end_date = fields.DateTimeField()
    employment_status = fields.EnumField(
        enum=EmploymentStatusChoices,
        default=EmploymentStatusChoices.ACTIVE
    )

    phone = fields.StringField(
        regex=r'^\+[1-9]\d{1,14}$',
        unique=True,
        required=True,
        help_text="Full international format (+countrycode...)",
        error_messages={'unique': "Phone number already registered"}
    )
    birthdate = fields.DateField(required=True)
    father_name = fields.StringField(max_length=200)
    # military_status = fields.EmbeddedDocumentField(MilitaryStatus, required=True)
    # degree_status = fields.EmbeddedDocumentField(DegreeStatus, required=True)
    #
    # marital_status = fields.EmbeddedDocumentField(MaritalStatus, required=True)
    child_number = fields.IntField(min_value=0, default=0)

    meta = {
        'collection': 'employees',
        'indexes': [
            {'fields': ['employment_id'], 'unique': True},
            {'fields': ['user'], 'unique': True},
            {'fields': ['position']},
            {'fields': ['birthdate']},
            {'fields': ['employment_start_date', 'employment_end_date']},
            {'fields': ['phone'], 'unique': True},
            {'fields': ['employment_status']}
        ],
        'ordering': ['employment_id'],
        'app_label': 'employees'
    }


    # @property
    # def department(self) -> Optional['Department']:
    #
    #     """
    #     Derived property to obtain the department from the employee's position.
    #
    #     Returns:
    #         The Department associated with the employee's position.
    #     """
    #
    #     return self.position.department

    def save(self, *args, **kwargs):
        if not self.employment_id:
            # Get and increment the max ID atomically
            max_id = Employee.objects.order_by('-employment_id').first()
            self.employment_id = (max_id.employment_id + 1) if max_id else 1000
        return super().save(*args, **kwargs)

    def clean(self) -> None:

        """
        Custom validation method for the Employee model.

        Validates:
          - Employment dates: End date (if provided) must not be before start date.
          - Birthdate: Must not be in the future.

        Raises:
            ValidationError: If any validation check fails.
        """
        #
        # # Prevent position department mismatch
        # if hasattr(self, 'position') and self.position.department != self.department:
        #     raise ValidationError("Employee position must match derived department")

        # Validate employment dates
        if self.employment_end_date and self.employment_end_date < self.employment_start_date:
            raise ValidationError("Employment end date cannot be before start date")

        # Validate birthdate
        if self.birthdate > timezone.now().date():
            raise ValidationError("Birthdate cannot be in the future")

    def __str__(self) -> str:

        """
        Returns a string representation of the employee.

        Returns:
            str: The full name from the associated user and the position title.
        """
        return f"{self.user.get_full_name()}"


