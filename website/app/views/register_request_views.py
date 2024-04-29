from ..forms import NewUserForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import json


def register_request(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        form = NewUserForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return JsonResponse({'status': 'OK'})
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return JsonResponse({'status': 'error', 'reason': 'Invalid data'})


def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        password = data['password']
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'OK'})
            else:
                return JsonResponse({'status': 'error', 'reason': 'Invalid username or password'})
        else:
            return JsonResponse({'status': 'error', 'reason': 'Missing username or password'})
    else:
        return JsonResponse({'status': 'error', 'reason': 'Invalid request method'})


def user_view(request):
    if request.user.is_authenticated:
        data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'date_joined': request.user.date_joined,
            'id': request.user.id,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'Пользователь не зарегистрирован'}, status=401)


def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'User logged out successfully'})


def forgot_password(request):
    if request.method == 'POST':
        pass
    else:
        return JsonResponse({'error': 'Invalid request method.'})
