from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.reverse import reverse


class CRUDTestsMixin:
    factory: DjangoModelFactory
    list_url_name: str
    detail_url_name: str
    model = None
    creation_data: dict
    put_data: dict
    client = None
    response = None
    object_in_database = None

    def test_create_ok(self):
        url = reverse(self.list_url_name)

        self.response = self.client.post(url, self.creation_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_delete_ok(self):
        existing_object = self.factory.create()
        url = reverse(self.detail_url_name, args=[existing_object.id])

        self.response = self.client.delete(url)

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
        result = self.model.objects.all()
        self.assertEqual(result.count(), 0)

    def test_list_ok(self):
        url = reverse(self.list_url_name)
        self.factory.create_batch(2)

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data), 2)

    def test_retrieve_ok(self):
        self.object_in_database = self.factory.create()
        url = reverse(self.detail_url_name, args=[self.object_in_database.id])

        self.response = self.client.get(url, vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_put_ok(self):
        self.object_in_database = self.factory.create()
        url = reverse(self.detail_url_name, args=[self.object_in_database.id])

        self.response = self.client.put(url, self.put_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.object_in_database = self.model.objects.get()

    def test_patch_ok(self):
        self.object_in_database = self.factory.create()
        url = reverse(self.detail_url_name, args=[self.object_in_database.id])

        self.response = self.client.patch(url, self.put_data, format='json', vHTTP_ACCEPT='application/json')

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.object_in_database = self.model.objects.get()
