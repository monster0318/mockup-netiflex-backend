import random
from django.utils.crypto import get_random_string
from user.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.template.loader import render_to_string
from config.config_settings import *


DOMAINS_END = [
        "test.com",
        "guest.com",
        "temp.com",
        "no-mail.com",
        "mock.com",
        "demo.com",
        "rnd-mail.com",
    ]

def message_body(reset_link, user_email):
    """
    This function render the email body for password reset using the template.
    """
    subject = "Videoflix Reset Password"
    context = {
        "username": "@" + user_email.split('@')[0] ,
        "reset_link": reset_link,
    }
    # Render the template with context
    message = render_to_string("reset_password.html", context)
    from_email=MAIL_USERNAME
    recipient_list=[user_email, MAIL_USERNAME]
    return subject,message,from_email,recipient_list

def is_guest_user(data) ->bool:
    """Check if the user is logging in as guest"""
    return data.get('email') == "guest@videoflix.com"


def is_guest_user_email(guest_email) ->bool:
    """Check if the email belongs to a guest user"""
    domain_end = guest_email.split('@')[1]
    return domain_end in DOMAINS_END


def generate_guest_email():
    """Generate random domain for guest email"""

    random_domain = random.choice(DOMAINS_END)
    email = f"videoflix-{get_random_string(6)}@{random_domain}" 
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
        )
        user.save()

        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)

        data = {
            "token": token.key,
            "email": user.email,
          
        }
        return data