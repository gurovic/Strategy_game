from django.http import HttpResponse
from django.shortcuts import render

from ..models import Tournament, PlayerInTournament


def start_page(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':

    return HttpResponse(f"Страница отображения результатов турнира {tournament_id}")
