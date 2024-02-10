from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from ..models import Tournament, PlayerInTournament


def register(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    user = request.user

    if request.method == 'POST':
        if len(tournament.players.all()) < tournament.max_of_players:
            tournament.players.add(user)
            return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'registered'})
        else:
            return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'denied registration'})
    else:
        if tournament.players.all().contains(user):
            return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'already registered'})
        else:
            return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'not registered'})
