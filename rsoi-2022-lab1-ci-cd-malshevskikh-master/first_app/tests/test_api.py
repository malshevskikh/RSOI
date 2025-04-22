import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Person
from ..serializers import PersonSerializer


# initialize the APIClient app
client = Client()

#Тестирование запроса get all
class GetAllPersonsTest(TestCase):

    def setUp(self):
        Person.objects.create(
            name='Max', age=22, address='Moscow', work='Programmer')
        Person.objects.create(
            name='Dominik', age=23, address='Vilnus', work='Artist')
        Person.objects.create(
            name='Ivan', age=18, address='Boston', work='Finance')

    def test_get_all_persons(self):
        # get API response
        response = client.get(reverse('get_post_person'))
        # get data from db
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#Тестирование запроса post
class PostNewPersonTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'name': 'Max',
            'age': 22,
            'address': 'Moscow',
            'work': 'Programmer'
        }

        self.invalid_data = {
            'name': '',
            'age': 23,
            'address': 'Vilnus',
            'work': ''
         }

    def test_post_valid_data(self):
        response = client.post(
            reverse('get_post_person'),
            data = json.dumps(self.valid_data),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_data(self):
        response = client.post(
            reverse('get_post_person'),
            data=json.dumps(self.invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#Тестирование запроса get по id
class GetPersonByIDTest(TestCase):

    def setUp(self):
        self.Max = Person.objects.create(
            name='Max', age=22, address='Moscow', work='Programmer')
        self.Dominik = Person.objects.create(
            name='Dominik', age=23, address='Vilnus', work='Artist')
        self.Ivan = Person.objects.create(
            name='Ivan', age=18, address='Boston', work='Finance')

    def test_get_by_id_valid_data(self):
        response = client.get(
            reverse('get_patch_delete_person', kwargs={'pk': self.Ivan.pk}))
        person = Person.objects.get(pk=self.Ivan.pk)
        serializer = PersonSerializer(person)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id_invalid_data(self):
        response = client.get(
            reverse('get_patch_delete_person', kwargs={'pk':1001}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#Тестирование запроса patch по id
class PatchPersonByIDTest(TestCase):

    def setUp(self):
        self.Max = Person.objects.create(
            name='Max', age=22, address='Moscow', work='Programmer')
        self.Dominik = Person.objects.create(
            name='Dominik', age=23, address='Vilnus', work='Artist')
        self.valid_data = {
            'name': 'Ivan',
            'age': 18,
            'address': 'Boston',
            'work': 'Finance'
        }
        self.invalid_data = {
            'name': '',
            'age': 20,
            'address': 'Moscow',
            'work': ''
         }

    def test_patch_by_id_valid_data(self):
        response = client.patch(
            reverse('get_patch_delete_person', kwargs={'pk': self.Dominik.pk}),
            data = json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_by_id_invalid_data(self):
        response = client.patch(
            reverse('get_patch_delete_person', kwargs={'pk': self.Dominik.pk}),
            data=json.dumps(self.invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#Тестирование запроса delete по id
class DeletePersonByIDTest(TestCase):

    def setUp(self):
        self.Max = Person.objects.create(
            name='Max', age=22, address='Moscow', work='Programmer')
        self.Dominik = Person.objects.create(
            name='Dominik', age=23, address='Vilnus', work='Artist')

    def test_delete_by_id_valid_data(self):
        response = client.delete(
            reverse('get_patch_delete_person', kwargs={'pk': self.Max.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_by_id_valid_data(self):
        response = client.delete(
            reverse('get_patch_delete_person', kwargs={'pk': 1001}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
