import factory
from factory.django import DjangoModelFactory

from applications.core.models.category import Category


class CategoriesFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('pystr')
