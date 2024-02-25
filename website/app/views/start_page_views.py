from django.shortcuts import render, redirect
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament
from ..views.tournaments_view import show

from django.contrib.auth.models import User
#кнопки: страница со всеми турнирами, кнопка создать турнир, приветственная фраза


def show_start_page(request):
    if request.method == 'POST':
        if request.POST['type'] == 'register':
            response = redirect('registration/')
            return response
        if request.POST['type'] == 'enter':
            return redirect('/accounts/login/')

        if request.POST['type'] == 'participate in tournament': #если надо зайти во все турниры
            if not request.user.is_authenticated:
                return redirect('/accounts/login/')
            return redirect('tournaments')
        if request.POST['type'] == 'create tournament':
            if not request.user.is_authenticated:
                return redirect('/accounts/login/')
            return redirect('tournament/create/')
        if request.POST['type'] == 'practice coding':
            if not request.user.is_authenticated:
                return redirect('/accounts/login/')
            return redirect('sandbox/')

    else:
        return render(request, 'start_page_views.html', {'status': 'show'})