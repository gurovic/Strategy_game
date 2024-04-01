from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from app.models import Tournament


def show(request):
    future_tournaments = list(Tournament.objects.filter(finish_registration_time__gte=timezone.now()).order_by("tournament_start_time", "finish_registration_time").values())
    past_tournaments = list(Tournament.objects.filter(finish_registration_time__lt=timezone.now()).order_by("-tournament_start_time", "finish_registration_time").values())

    return JsonResponse({'future': future_tournaments, 'past': past_tournaments})
