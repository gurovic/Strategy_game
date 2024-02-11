from django.http import HttpResponse
from django.shortcuts import render

from ..models import Tournament, PlayerInTournament


def show(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except:
        return HttpResponse("This tournament does not exist")

    players_in_tournament = PlayerInTournament.objects.filter(tournament=tournament).order_by("place", "-number_of_points")

    return render(request, 'tournament_results.html', {'tournament':tournament, 'players_in_tournament':players_in_tournament})
