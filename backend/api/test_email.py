from django.core.mail import send_mail

def send_test_email():
    subject = 'Test Email'
    message = 'This is a test email sent using SMTP in Django.'
    from_email = 'sunnytheater.contact@gmail.com'
    recipient_list = ['georgianaioanacojocaru@gmail.com']

    send_mail(subject, message, from_email, recipient_list)

if __name__ == "__main__":
    send_test_email()