from app.models import Tournament
from django.shortcuts import render, redirect


def show(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':
        if request.POST['type'] == 'register':
            return redirect('tournament/<int:tournament_id>/registration')
