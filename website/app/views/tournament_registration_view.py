from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from app.models.tournament import Tournament


def register(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    user = request.user

    if tournament.players.all().contains(user):
        return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'already registered'})
    elif len(tournament.players.all()) >= tournament.max_of_players:
        return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'denied registration'})

    if request.method == 'POST':
        tournament.players.add(user)
        return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'registered'})
    else:
        return render(request, 'tournament_registration.html', {'tournament': tournament, 'status': 'not registered'})
