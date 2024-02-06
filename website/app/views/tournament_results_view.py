from django.http import HttpResponse
from django.shortcuts import render

from ..models import Tournament, PlayerInTournament


def start_page(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except:
        return HttpResponse("This tournament does not exist")

    players = PlayerInTournament.objects.filter(tournament=tournament)

    return render(request, 'tournament_results.html', {'tournament':tournament, 'players':players})
