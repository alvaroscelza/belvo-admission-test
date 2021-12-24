from rest_framework.test import APITestCase

from applications.core.models import UserTransaction
from applications.core.tests.crud_tests_mixin import CRUDTestsMixin
from applications.core.tests.factories.user_transactions_factories import UserTransactionsFactory


class UserTransactionTests(CRUDTestsMixin, APITestCase):
    factory = UserTransactionsFactory
    list_url_name = 'user_transactions-list'
    detail_url_name = 'user_transactions-detail'
    model = UserTransaction

    def setUp(self):
        super().setUp()
        self.creation_data = {'reference': '000051', 'date': '2020-01-13', 'amount': '-51.13', 'type': 'outflow',
                              'category': 'groceries', 'user_email': 'janedoe@email.com'}
        self.put_data = {'reference': '000051', 'date': '2020-01-13', 'amount': '100', 'type': 'outflow',
                         'category': 'groceries', 'user_email': 'janedoe@email.com'}
