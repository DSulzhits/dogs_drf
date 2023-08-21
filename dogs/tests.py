from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from dogs.models import Breed, Dog
from users.models import User, UserRoles


class DogTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='tester',
            email='tester@test1.com',
            role=UserRoles.MODERATOR,
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        self.user.set_password('qwerty')
        self.user.save()
        response = self.client.post('/users/token/', {"email": "tester@test1.com", "password": "qwerty"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.breed = Breed.objects.create(
            name='test',
            description='testing_breed'
        )

        self.dog = Dog.objects.create(
            name='test',
            breed=self.breed
        )

    def test_get_list(self):
        """Test for getting list of dogs"""

        response = self.client.get(
            reverse('dogs:dog_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": self.dog.name,
                        "breed": self.dog.breed.name
                    }
                ]
            }
        )

    def test_dog_create(self):
        """Test dog creating"""
        data = {
            'name': 'test2',
            'category': self.breed.id
        }

        response = self.client.post(
            reverse('dogs:dog_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Dog.objects.all().count(),
            2
        )

    def test_dog_create_validation_error(self):
        """Test validation error"""
        data = {
            'name': 'крипта',
            'category': self.breed.id
        }

        response = self.client.post(
            reverse('dogs:dog_create'),
            data=data
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'name': ['Использованы запрещенные слова!']}
        )
