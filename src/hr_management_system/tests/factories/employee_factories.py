from datetime import timedelta

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
    gender = GenderStatusChoices.MALE  # or use the enum value if defined, e.g. GenderStatusChoices.M.value
    position = factory.SubFactory(PositionFactory)
    employment_start_date = factory.LazyFunction(lambda: timezone.now() - timedelta(days=365))
    employment_end_date = factory.LazyFunction(timezone.now)
    employment_status = EmploymentStatusChoices.ACTIVE  # or EmploymentStatusChoices.ACTIVE.value
    phone = factory.Faker("numerify", text="+1##########")
    birthdate = factory.LazyFunction(lambda: timezone.now().date() - timedelta(days=365*30))
    father_name = factory.Faker("name")
    military_status = factory.LazyFunction(
        lambda: MilitaryStatus(status=MilitaryStatus.StatusChoices.EXEMPT, document=None)
    )
    degree_status = factory.LazyFunction(
        lambda: DegreeStatus(status=DegreeStatus.StatusChoices.BACHELOR, document=None)
    )
    marital_status = factory.LazyFunction(
        lambda: MaritalStatus(status=MaritalStatus.StatusChoices.SINGLE, document=None)
    )
    child_number = 0


# class MilitaryStatusFactory(factory.mongoengine.MongoEngineFactory):
#     class Meta:
#         model = MilitaryStatus
#
#     status = fuzzy.FuzzyChoice(['exempt', 'completed', 'postponed'])
#     # For file fields, use dummy data
#     document = factory.LazyAttribute(lambda _: b"dummy_file_content")
#
#
# class MaritalStatusFactory(factory.mongoengine.MongoEngineFactory):
#     class Meta:
#         model = MaritalStatus
#
#     status = fuzzy.FuzzyChoice(['single', 'married', 'divorced'])
#     document = factory.LazyAttribute(lambda _: b"dummy_file_content")
#
#
# class DegreeStatusFactory(factory.mongoengine.MongoEngineFactory):
#     class Meta:
#         model = DegreeStatus
#
#     status = fuzzy.FuzzyChoice(['bachelor', 'master', 'doctorate', 'other'])
#     document = factory.LazyAttribute(lambda _: b"dummy_file_content")
#
#
# class EmployeeFactory(factory.mongoengine.MongoEngineFactory):
#     class Meta:
#         model = Employee
#
#     employment_id = factory.Sequence(lambda n: 1000 + n)
#     user = factory.SubFactory('tests.factories.UserFactory')  # Create UserFactory separately
#     gender = fuzzy.FuzzyChoice(['M', 'F', 'O'])
#     position = factory.SubFactory('tests.factories.PositionFactory')
#     employment_start_date = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(days=365))
#     phone = fuzzy.FuzzyText(prefix='+', length=12)
#     birthdate = fuzzy.FuzzyDate(timezone.datetime(1970, 1, 1).date())
#     father_name = factory.Faker('first_name')
#     military_status = factory.SubFactory(MilitaryStatusFactory)
#     degree_status = factory.SubFactory(DegreeStatusFactory)
#     marital_status = factory.SubFactory(MaritalStatusFactory)
#     child_number = fuzzy.FuzzyInteger(0, 5)
#
#     class Params:
#         terminated = factory.Trait(
#             employment_status='terminated',
#             employment_end_date=factory.LazyFunction(timezone.now)
#         )
#         future_birthdate = factory.Trait(
#             birthdate=factory.Faker('future_date')
#         )
