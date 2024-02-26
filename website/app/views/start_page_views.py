from django.shortcuts import render, redirect
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament
from ..views.tournaments_view import show

from django.contrib.auth.models import User
#кнопки: страница со всеми турнирами, кнопка создать турнир, приветственная фраза


def show_start_page(request):
    user = None
    if request.method == 'POST':
        return render(request, 'start_page_views.html', {'status': 'error'})
    else:
        return render(request, 'start_page_views.html', {'status': 'show'})