from datetime import datetime

import factory
from factory.django import DjangoModelFactory

from applications.core.models import UserTransaction


class UserTransactionsFactory(DjangoModelFactory):
    class Meta:
        model = UserTransaction

    reference = factory.Faker('pystr', max_chars=6)
    date = datetime.now()
    amount = 100
    type = UserTransaction.TransactionTypes.INFLOW
    category = 'groceries'
    user_email = factory.Faker('email')
