import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from src.hr_management_system.departments.models import Department, Position


class DepartmentFactory(MongoEngineFactory):

    """
    Factory for generating Department model instances.

    This factory creates Department objects with random but realistic values:
      - `code`: A random string with a "DEPT-" prefix.
      - `name`: A fake word generated by Faker.
      - `headcount`: Initialized to 0.
    """

    class Meta:
        model = Department

    code = fuzzy.FuzzyText(
        length=5, prefix="DEPT-", chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    )
    name = factory.Faker("word", locale="en_US")
    headcount = 0


class PositionFactory(factory.mongoengine.MongoEngineFactory):

    """
    Factory for generating Position model instances.

    This factory creates Position objects with realistic data:
      - `title`: A fake job title generated by Faker.
      - `department`: Automatically creates a Department using DepartmentFactory.
      - `description`: A fake sentence describing the position.
      - `is_active`: Defaults to True.
    """

    class Meta:
        model = Position

    title = factory.Faker("job")
    department = factory.SubFactory(DepartmentFactory)
    description = factory.Faker("sentence")
    is_active = True
