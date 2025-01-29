import random
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.template.loader import render_to_string
from config.config_settings import *

def message_body(username, reset_link, user_email):
    """
    This function render the email body for password reset using the template.
    """
    subject = "Join Password Reset"
    context = {
        "username": username,
        "reset_link": reset_link,
    }
    # Render the template with context
    message = render_to_string("emails/password_reset.html", context)
    from_email=MAIL_USERNAME
    recipient_list=[user_email, MAIL_USERNAME]
    return subject,message,from_email,recipient_list

def is_guest_user(data):
    return data['email'] == "guest@videoflix.com"

def generate_guest_email():
    """Generate random domain for guest email"""
    domains = [
        "test.com",
        "guest.com",
        "temp.com",
        "no-mail.com",
        "mock.com",
        "demo.com",
        "rnd-mail.com",
    ]

    random_domain = random.choice(domains)
    email = f"coderr-{get_random_string(6)}@{random_domain}" 
    return email

def generate_guest_username():
    """Genarate random username for guest users"""
    names = [
        "Guest",
        "Demo",
        "Gast"
    ]

    random_name = random.choice(names)
    username = f"{random_name}-{get_random_string(6)}" 
    return username



def guest_login(request):
        """Login guest users"""
        user = User.objects.create_user(
            email=generate_guest_email(),
            username=generate_guest_username()
        )
        user.save()

        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)

        data = {
            "token": token.key,
            "email": user.email,
            "username": user.username,
          
        }
        return data