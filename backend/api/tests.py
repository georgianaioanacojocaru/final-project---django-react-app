from django.test import TestCase

# Create your tests here.

from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'sunnytheter.contact@gmail.com',  # Sender's email
    ['georgianaioanacojocaru@gmail.com'],  # List of recipients
    fail_silently=False,
)