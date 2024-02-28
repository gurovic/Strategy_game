from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from app.models import Tournament, Game


def show(request):
    available_games = Game.objects.all()
    return render(request, 'sandbox_all_games.html',
                  {'available_games': available_games})

