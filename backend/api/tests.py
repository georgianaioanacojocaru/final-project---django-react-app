import json
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from backend.api.models import Movie
from backend.api.serializers import MovieSerializer
from backend.api.views import get_movies

# Create your tests here.

class GetMoviesAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()

    def test_get_movies(self):
        # Create a user and authenticate
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)

        # Create some movies for testing
        movie1 = Movie.objects.create(title="Movie 1")
        movie2 = Movie.objects.create(title="Movie 2")

        # Create a request object
        url = '/api/movies/'
        request = self.factory.get(url)
        request.user = user

        # Call the API view
        response = get_movies(request)

        # Check response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response data
        expected_data = {
            'message': "Everything went successful",
            'movies': MovieSerializer([movie1, movie2], many=True, context={'request': request}).data
        }
        self.assertEqual(json.loads(response.content), expected_data)