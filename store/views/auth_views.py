from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings
from pathlib import Path
from dotenv import load_dotenv
import os
import requests

# Load .env file for hCaptcha keys
env_path = Path(__file__).resolve().parent.parent.parent / 'popcorn_box' / '.env'
if env_path.exists():
    load_dotenv(env_path)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Try to get user by email (Django's default User model uses username, but we can use email)
            user = User.objects.get(email=email)
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, _('Login successful! Welcome back.'))
                return redirect('home')
            else:
                messages.error(request, _('Invalid email or password.'))
        except User.DoesNotExist:
            messages.error(request, _('Invalid email or password.'))
    return render(request, 'login.html', {'title': _('Sign In')})

def logout_view(request):
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        hcaptcha_response = request.POST.get('h-captcha-response')

        # Validation
        if password != password_confirm:
            messages.error(request, _('Passwords do not match.'))
        elif User.objects.filter(username=username).exists():
            messages.error(request, _('Username already exists.'))
        elif User.objects.filter(email=email).exists():
            messages.error(request, _('Email already exists.'))
        elif len(password) < 6:
            messages.error(request, _('Password must be at least 6 characters.'))
        else:
            # Validate hCaptcha manually
            hcaptcha_response = request.POST.get('h-captcha-response')
            if not hcaptcha_response:
                messages.error(request, _('Please complete the CAPTCHA.'))
            else:
                # Use the same validation method as django-hcaptcha package
                from urllib.error import HTTPError
                from urllib.parse import urlencode
                from urllib.request import build_opener, Request, ProxyHandler
                import json
                
                VERIFY_URL = 'https://hcaptcha.com/siteverify'
                TIMEOUT = 10  # seconds
                HCAPTCHA_SECRET_KEY = os.getenv('HCAPTCHA_SECRET_KEY', '0x0000000000000000000000000000000000000000')
                opener = build_opener(ProxyHandler({}))
                post_data = urlencode({
                    'secret': HCAPTCHA_SECRET_KEY,
                    'response': hcaptcha_response,
                }).encode()
                request_captcha = Request(VERIFY_URL, post_data)
                try:
                    response = opener.open(request_captcha, timeout=TIMEOUT)
                    response_data = json.loads(response.read().decode("utf-8"))
                    
                    if not response_data.get('success'):
                        messages.error(request, _('Invalid CAPTCHA. Please try again.'))
                        return render(request, 'signup.html', {
                            'title': _('Sign Up'),
                            'HCAPTCHA_SITE_KEY': os.getenv('HCAPTCHA_SITE_KEY', '10000000-ffff-ffff-ffff-000000000001')
                        })
                except HTTPError:
                    messages.error(request, _('CAPTCHA verification failed. Please try again.'))
                    return render(request, 'signup.html', {
                        'title': _('Sign Up'),
                        'HCAPTCHA_SITE_KEY': os.getenv('HCAPTCHA_SITE_KEY', '10000000-ffff-ffff-ffff-000000000001')
                    })
                
                # If we get here, CAPTCHA is valid - create the user
                # Créer l'utilisateur (actif immédiatement)
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_active=True  # Compte actif immédiatement
                )
                
                # Créer le profil utilisateur
                from ..models import UserProfile
                user_profile = UserProfile.objects.create(
                    user=user,
                    language='en'
                )

                # Connecter l'utilisateur automatiquement
                login(request, user)
                messages.success(request, _('Account created successfully! Welcome to Popcorn Box!'))
                return redirect('home')

    return render(request, 'signup.html', {
        'title': _('Sign Up'),
        'HCAPTCHA_SITE_KEY': os.getenv('HCAPTCHA_SITE_KEY', '10000000-ffff-ffff-ffff-000000000001')
    })