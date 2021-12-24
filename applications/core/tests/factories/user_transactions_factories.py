from datetime import datetime

import factory
from factory.django import DjangoModelFactory

from applications.core.models import UserTransaction
from applications.core.tests.factories.categories_factories import CategoriesFactory


class UserTransactionsFactory(DjangoModelFactory):
    class Meta:
        model = UserTransaction

    reference = factory.Faker('pystr')
    date = datetime.now()
    amount = 100
    type = UserTransaction.TransactionTypes.INFLOW
    category = factory.SubFactory(CategoriesFactory)
    user_email = factory.Faker('pystr')
