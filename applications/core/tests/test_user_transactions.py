from rest_framework import status
from rest_framework.reverse import reverse
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

    def test_create_bunch_ok(self):
        url = reverse(self.list_url_name)
        create_bulk_url = '{}create_bulk/'.format(url)
        creation_bulk = [
            {'reference': '000001', 'date': '2020-01-13', 'amount': '-51.13', 'type': 'outflow',
             'category': 'groceries', 'user_email': 'janedoe@email.com'},
            {'reference': '00002', 'date': '2020-01-13', 'amount': '100', 'type': 'inflow',
             'category': 'groceries', 'user_email': 'janedoe@email.com'}
        ]

        self.response = self.client.post(create_bulk_url, creation_bulk, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        all_transactions = UserTransaction.objects.all()
        self.assertEqual(len(all_transactions), len(creation_bulk))

    def test_create_duplicated_transaction_should_return_error(self):
        self.factory.create(reference='000051')
        url = reverse(self.list_url_name)

        self.response = self.client.post(url, self.creation_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(self.response.data['reference'][0]), 'Ya existe user transaction con este reference.')

    def test_inflow_negative_transaction_should_return_error(self):
        self.creation_data['type'] = 'inflow'
        url = reverse(self.list_url_name)

        self.response = self.client.post(url, self.creation_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(self.response.data[0]), 'All inflow transactions amounts are positive decimal numbers.')

    def test_outflow_positive_transaction_should_return_error(self):
        self.creation_data['amount'] = '100'
        url = reverse(self.list_url_name)

        self.response = self.client.post(url, self.creation_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(self.response.data[0]), 'All outflow transactions amounts are negative decimal numbers.')
