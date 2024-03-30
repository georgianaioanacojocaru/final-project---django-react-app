import json
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from backend.api.models import Movie, Comment, Seat
from backend.api.serializers import MovieSerializer
from backend.api.views import get_movies

class GetMoviesAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.movie = Movie.objects.create(title='Test Movie')
        self.movie_2 = Movie.objects.create(title='The Godfather')
        self.movie_3 = Movie.objects.create(title='The Matrix')
        self.comment = Comment.objects.create(movie=self.movie)
        self.seat1 = Seat.objects.create(seat_number='A1')
        self.seat2 = Seat.objects.create(seat_number='A2')



    def test_get_movies(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)

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

    def test_get_movie_success(self):
        response = self.client.get(f'/get_movie/{self.movie.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Everything went successful')
        self.assertEqual(response.json()['movie']['title'], 'Test Movie')
        self.assertEqual(len(response.json()['comments']), 1)  # Assuming only one comment for simplicity

    def test_get_seats(self):
        response = self.client.get(f'/get_seats/{self.movie.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNone(response.json()['message'])
        self.assertEqual(len(response.json()['reserved_seats']), 1)
        self.assertEqual(len(response.json()['all_seats']), 2)

    def test_book_seat(self):
        data = {
            'seat_id': self.seat.id,
            'movie_id': self.movie.id,
        }

        response = self.client.post('/book_seat/', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'You have successfully booked a seat')
        self.assertTrue(self.movie.reserved_seats.filter(id=self.seat.id).exists())
        self.assertEqual(self.movie.tickets, 4)

    def test_search_movie_success(self):
        query = 'the'
        # Make GET request to search_movie endpoint with query
        response = self.client.get(f'/search_movie/?query={query}')
        # Check response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response data
        self.assertEqual(response.json()['message'], 'Everything was successful')
        self.assertEqual(len(response.json()['movies']), 2)  # Expecting 2 movies containing 'the'

    def test_create_comment(self):
        data = {
            'movie_id': self.movie.id,
            'content': 'Great movie!',
        }
        response = self.client.post('/create_comment/', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Everything was successful')
        self.assertTrue(Comment.objects.filter(movie=self.movie, content='Great movie!', username='JohnDoe').exists())

    def test_get_comments(self):
        response = self.client.get(f'/get_comments/{self.movie.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Everything went successfully')
        self.assertEqual(len(response.json()['comments']), 2)  # Assuming there are two comments for the movie
