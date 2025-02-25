from datetime import timedelta
from typing import Dict

import factory
from django.utils import timezone
from factory.mongoengine import MongoEngineFactory

from src.hr_management_system.employees.models import (
    DegreeStatus, Employee, EmploymentStatusChoices,
    GenderStatusChoices, MaritalStatus, MilitaryStatus
)
from src.hr_management_system.tests.factories.department_factories import PositionFactory
from src.hr_management_system.tests.factories.user_factories import BaseUserFactory


class EmployeeFactory(MongoEngineFactory):

    class Meta:
        model = Employee

    user = factory.SubFactory(BaseUserFactory)
    # gender = GenderStatusChoices.MALE
    # position = factory.SubFactory(PositionFactory)
    employment_start_date = factory.LazyFunction(lambda: timezone.now() - timedelta(days=365))
    employment_end_date = factory.LazyFunction(timezone.now)
    employment_status = EmploymentStatusChoices.ACTIVE
    phone = factory.Faker("numerify", text="+1##########")
    birthdate = factory.LazyFunction(lambda: timezone.now().date() - timedelta(days=365*30))
    father_name = factory.Faker("name")
    # military_status = factory.LazyFunction(
    #     lambda: MilitaryStatus(status=MilitaryStatus.StatusChoices.EXEMPT, document=None)
    # )
    # degree_status = factory.LazyFunction(
    #     lambda: DegreeStatus(status=DegreeStatus.StatusChoices.BACHELOR, document=None)
    # )
    # marital_status = factory.LazyFunction(
    #     lambda: MaritalStatus(status=MaritalStatus.StatusChoices.SINGLE, document=None)
    # )
    child_number = 0

    @classmethod
    def create_payload(cls) -> Dict[str, str]:

        """
        A class method that generates a payload dictionary for creating
        a user via the API.
        :return: generate a payload dictionary with consistent values
        for creating users via the API.
        """

        test_employee = cls.build()
        return {
            'email': test_employee.user.email,
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            # 'gender': test_employee.gender.value,
            # 'position': test_employee.position,
            'employment_start_date': test_employee.employment_start_date,
            'birthdate': test_employee.birthdate,
            'phone': test_employee.phone,
            'father_name': test_employee.father_name,
            # 'military_status': MilitaryStatus.StatusChoices.EXEMPT.value,
            # 'degree_status': DegreeStatus.StatusChoices.BACHELOR.value,
            'child_number': test_employee.child_number,
        }
