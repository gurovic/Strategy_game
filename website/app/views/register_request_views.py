from django.shortcuts import render, redirect
from ..forms import NewUserForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
