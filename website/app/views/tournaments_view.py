from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from app.models import Tournament


def show(request):
    upcoming_or_current_tournaments = Tournament.objects.filter(end_time__gte=timezone.now()).order_by("tournament_start_time", "finish_registration_time")
    past_tournaments = Tournament.objects.filter(end_time__lt=timezone.now()).order_by("-tournament_start_time", "finish_registration_time")

    return render(request, 'tournaments.html',
                  {'upcoming_or_current_tournaments': upcoming_or_current_tournaments, 'past_tournaments': past_tournaments})
