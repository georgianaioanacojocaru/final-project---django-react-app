from .models import * 
from .serializers import * 
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import status 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movies(request):
    message = "Everything went successful"
    response_status = status.HTTP_200_OK
    movies = Movie.objects.all()
    movies = MovieSerializer(movies, many=True, context={'request': request})

    return Response({'message':message, 'movies':movies.data}, status=response_status)

@api_view(['POST'])
def register(request):
    message = "Nothing until this point"
    response_status = status.HTTP_304_NOT_MODIFIED

    request = json.loads(request.body)
    first_name = request.get('first_name')
    last_name = request.get('last_name')
    email = request.get('email')
    password = request.get('password')

    if first_name is not None and last_name is not None and password is not None and email is not None:
        message = "All parameters were provided"

        user = authenticate(request, username=email, password=password)
        print(user)
        if user:
            print(user)
            message = "Email already in use"
            response_status = status.HTTP_400_BAD_REQUEST

        if user is None:
            password = make_password(password=password)
            new_user = MyUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            new_user.save()
            message = "User has been created successfully"
            response_status = status.HTTP_200_OK

    return Response({'message':message}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movie(request, id):
    message = 'Everything went successful'
    response_status = status.HTTP_200_OK
    comments = None
    movie = None

    if id:
        id = int(id)
        movie = Movie.objects.get(id=id)
        comments = Comment.objects.filter(movie=movie)
        comments = CommentSerializer(comments, many=True)
        if movie is not None:
            movie = MovieSerializer(movie, many=False, context={'request': request})
    else:
        message = "Movie id not provided"
        response_status = status.HTTP_204_NO_CONTENT

    return Response({'message':message, 'movie':movie.data, 'comments':comments.data}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seats(request, id):
    message = None 
    response_status = None 

    if id:
        id = int(id)
        movie = Movie.objects.get(id=id)
        reserved_seats = movie.reserved_seats.all()
        reserved_seats = SeatSerializer(reserved_seats, many=True)
        all_seats = Seat.objects.all()
        all_seats = SeatSerializer(all_seats, many=True)
        response_status = status.HTTP_200_OK
        return Response({'message':message, 'reserved_seats':reserved_seats.data, 'all_seats':all_seats.data}, status=response_status)    

    message = "Something went wrong"
    response_status =  status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response({'message':message}, status=response_status)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_seat(request):
    message = None
    user = request.user
    req_data = json.loads(request.body)

    seat_id = req_data.get('seat_id')
    movie_id = req_data.get('movie_id')

    if not (seat_id and movie_id):
        return Response({'message': 'Both seat_id and movie_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        movie = Movie.objects.get(id=movie_id)
        seat = Seat.objects.get(id=seat_id)

        if seat in movie.reserved_seats.all():
            return Response({'message': 'Seat is already booked'}, status=status.HTTP_400_BAD_REQUEST)

        if movie.tickets_available > 0:
            movie.reserved_seats.add(seat)
            movie.tickets -= 1
            movie.save()

            send_mail(
                'Seat Booking Confirmation',
                f'You have successfully booked a seat for the movie {movie.title} on date {movie.date_time}. Your seat is {seat.name}. Thank you for your interest',
                'sunnytheater.contact@gmail.com',  
                [user.email],
                fail_silently=False,
            )
            message = "You have successfully booked a seat"
            
            if movie.tickets == 0:
                movie.tickets_available = False
                movie.save()
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tickets available for this movie'}, status=status.HTTP_400_BAD_REQUEST)

    except Movie.DoesNotExist:
        return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    except Seat.DoesNotExist:
        return Response({'message': 'Seat not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movie(request):
    message = None 
    query = request.GET.get('query')
    response_status = None 
    if query is not None:
        query = str(query)
        movies = Movie.objects.filter(title__icontains=query)
        movies = MovieSerializer(movies, many=True, context={'request': request})
        message = "Everything was successful"
        response_status = status.HTTP_200_OK
    else:
        response_status = status.HTTP_400_BAD_REQUEST
        message = 'Search query not provided'
    return Response({'message':message, 'movies':movies.data}, status=response_status)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    response_status = None 
    message = None
    user = request.user
    request_body = json.loads(request.body)
    movie_id = request_body.get('movie_id')
    if movie_id:
        movie_id = int(movie_id)
        content = request_body.get('content')
        username = user.first_name + user.last_name 
        movie = Movie.objects.get(id=movie_id)

        new_comment = Comment.objects.create(
            content=content,
            username=username,
            movie=movie,
        )

        new_comment.save()
        response_status = status.HTTP_200_OK
        message = "Everything was successful"
    else:
        response_status = status.HTTP_400_BAD_REQUEST
        message = 'Movie Id was not provided'

    return Response({'message':message}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(request, id):
    message = None 
    response_status = status.HTTP_304_NOT_MODIFIED

    if id:
        id = int(id)
        movie = Movie.objects.get(id=id)
        comments = Comment.objects.filter(movie=movie)
        comments = CommentSerializer(comments, many=True)
        message = "Everything went successfully"
        response_status = status.HTTP_200_OK

    elif id is None:
        message = "Movie Id was not provided"
        response_status = status.HTTP_400_BAD_REQUEST

    else:
        message = "Something went wrong"
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response({'message':message, 'comments':comments.data}, status=response_status)

