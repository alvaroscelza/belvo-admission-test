from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from applications.core.tests.factories.categories_factories import CategoriesFactory


class UserTransactionTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.category = CategoriesFactory.create()
        self.list_url_name = 'user_transactions-list'

    def test_create_ok(self):
        url = reverse(self.list_url_name)
        self.creation_data = {'reference': '000051', 'date': '2020-01-13', 'amount': '-51.13', 'type': 'outflow',
                              'category': 'groceries', 'user_email': 'janedoe@email.com'}

        self.response = self.client.post(url, self.creation_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.data['reference'], '000051')
        self.assertEqual(self.response.data['date'], '')
        self.assertEqual(self.response.data['amount'], -51.13)
        self.assertEqual(self.response.data['type'], 'outflow')
        self.assertEqual(self.response.data['category'].name, 'category')
        self.assertEqual(self.response.data['user_email'], 'janedoe@email.com')
