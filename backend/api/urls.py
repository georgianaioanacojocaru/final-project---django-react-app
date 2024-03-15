from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register'),
    path('get-movies/', views.get_movies, name='get-movies'),
    path('get-movie/<id>', views.get_movie, name='get-movie'),
    path('get-seats/<id>', views.get_seats, name='get-seats'),
    path('book-seat/', views.book_seat, name='book-seat'),
    path('search-movies/', views.search_movie, name='search-movies'),
    path('create-comment/', views.create_comment, name='create-comment'),
    path('get-comments/<id>', views.get_comments, name='get-comments'),
]