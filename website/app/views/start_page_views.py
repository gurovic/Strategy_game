from django.shortcuts import render, redirect
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament
from ..views.tournaments_view import show

from django.contrib.auth.models import User
#кнопки: страница со всеми турнирами, кнопка создать турнир, приветственная фраза
def show_start_page(request):
    user = request.user
    if request.method == 'POST':
        if request.POST['type'] == 'all tournaments': #если надо зайти во все турниры
            response = redirect('tournaments')
            return response
        if request.POST['type'] == 'create tournament':
            response = redirect('tournament/create/')
            return response
    else:
        return render(request, 'start_page_views.html')