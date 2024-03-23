from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Seat(models.Model):

    name = models.CharField(max_length=100, verbose_name="Seat Name/Title", null=False, default='')    

    def __str__(self):

        return self.name

class Movie(models.Model):

    title = models.CharField(max_length=100, verbose_name='Movie Title')
    reserved_seats = models.ManyToManyField(to=Seat, verbose_name='Reserved Seats', null=True)
    price = models.FloatField(default=1, null=False)
    img = models.ImageField(default='', verbose_name='Movie Cover Image', upload_to='movie_covers', null=False, blank=False)
    tickets = models.PositiveIntegerField(null=False, verbose_name='Available Tickets')
    booked_tickets = models.IntegerField(null=False, default=0, verbose_name='Booked Tickets')
    description = models.TextField(verbose_name='Brief Description')
    trailer_link = models.CharField(max_length=1000000, verbose_name="Movie Trailer Link", null=True, blank=True)
    tickets_available = models.BooleanField(default=True, verbose_name="Tickets Available")
    date_time = models.DateTimeField(null=False,verbose_name='Scheduled On')

    def __str__(self):

        return self.title


class Comment(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    username = models.CharField(verbose_name="User", max_length=400)
    content = models.TextField(verbose_name='Content')
    date = models.DateField(auto_now=True, null=False, verbose_name="Date")

    def __str__(self):

        return self.movie.title
