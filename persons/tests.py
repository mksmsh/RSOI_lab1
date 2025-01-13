from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Person


class PersonAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person_data = {
            "name": "Alice",
            "age": 30,
            "address": "123 Main St",
            "work": "Engineer"
        }
        self.person = Person.objects.create(**self.person_data)

    def test_get_all_persons(self):
        response = self.client.get('/api/v1/persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # В базе одна запись
        self.assertEqual(response.data[0]['name'], "Alice")

    def test_get_person_by_id(self):
        response = self.client.get(f'/api/v1/persons/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Alice")

    def test_get_person_not_found(self):
        response = self.client.get('/api/v1/persons/999/')  # Несуществующий ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person(self):
        new_person_data = {
            "name": "Bob",
            "age": 25,
            "address": "456 Elm St",
            "work": "Artist"
        }
        response = self.client.post('/api/v1/persons/', new_person_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Location', response.headers)  # Проверка заголовка Location

    def test_update_person(self):
        update_data = {"address": "789 Oak St"}
        response = self.client.patch(f'/api/v1/persons/{self.person.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.person.refresh_from_db()
        self.assertEqual(self.person.address, "789 Oak St")

    def test_delete_person(self):
        response = self.client.delete(f'/api/v1/persons/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Person.objects.filter(id=self.person.id).exists())

