from django.http import HttpResponse
from django.shortcuts import render

from ..models import Tournament, PlayerInTournament


def show(request):
    tournaments = Tournament.objects.all()

    return render(request, 'tournaments.html', {'tournaments':tournaments})
