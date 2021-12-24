from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from applications.core.models import UserTransaction
from applications.core.tests.crud_tests_mixin import CRUDTestsMixin
from applications.core.tests.factories.user_transactions_factories import UserTransactionsFactory
from applications.core.tests.test_data import example_input


class UserTransactionTests(CRUDTestsMixin, APITestCase):
    factory = UserTransactionsFactory
    list_url_name = 'transactions-list'
    detail_url_name = 'transactions-detail'
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

    def test_total_inflow_and_outflow_per_user(self):
        test_data = example_input
        for data in test_data:
            self.factory.create(**data)
        url = reverse(self.list_url_name)
        url = '{}types_per_user/'.format(url)

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        expected_data = [
            {
                'user_email': 'janedoe@email.com',
                'total_inflow': '2651.44',
                'total_outflow': '-761.85'
            },
            {
                'user_email': 'johndoe@email.com',
                'total_inflow': '0.00',
                'total_outflow': '-51.13'
            }
        ]
        self.assertEqual(self.response.data[0]['user_email'], expected_data[0]['user_email'])
        self.assertEqual(float(self.response.data[0]['total_inflow']), float(expected_data[0]['total_inflow']))
        self.assertEqual(float(self.response.data[0]['total_outflow']), float(expected_data[0]['total_outflow']))
        self.assertEqual(self.response.data[1]['user_email'], expected_data[1]['user_email'])
        self.assertEqual(float(self.response.data[1]['total_inflow']), float(expected_data[1]['total_inflow']))
        self.assertEqual(float(self.response.data[1]['total_outflow']), float(expected_data[1]['total_outflow']))

    def test_user_summary(self):
        test_data = example_input
        for data in test_data:
            self.factory.create(**data)
        url = reverse(self.list_url_name)
        url = '{}user_summary/?user_email=janedoe@email.com'.format(url)

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        expected_data = {
            'inflow': {
                'salary': '2500.72',
                'savings': '150.72'
            },
            'outflow': {
                'groceries': '-51.13',
                'rent': '-560.00',
                'transfer': '-150.72'
            }
        }
        self.assertEqual(float(self.response.data['inflow']['salary']), float(expected_data['inflow']['salary']))
        self.assertEqual(float(self.response.data['inflow']['savings']), float(expected_data['inflow']['savings']))
        self.assertEqual(float(self.response.data['outflow']['groceries']),
                         float(expected_data['outflow']['groceries']))
        self.assertEqual(float(self.response.data['outflow']['rent']), float(expected_data['outflow']['rent']))
        self.assertEqual(float(self.response.data['outflow']['transfer']), float(expected_data['outflow']['transfer']))

    def test_user_summary_error_missing_user_email(self):
        url = reverse(self.list_url_name)
        url = '{}user_summary/'.format(url)

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response.data, 'user_email is required.')
