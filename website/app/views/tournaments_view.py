from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from ..models import Tournament


def show(request):
    tournaments = Tournament.objects.order_by("start_time", "end_time")
    upcoming_or_current_tournaments = tournaments.filter(end_time__gte=timezone.now())
    past_tournaments = tournaments.filter(end_time__lt=timezone.now())

    return render(request, 'tournaments.html',
                  {'upcoming_or_current_tournaments': upcoming_or_current_tournaments, 'past_tournaments': past_tournaments})
