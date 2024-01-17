from django.shortcuts import render
from ..models import Tournament, PlayerInTournament
from django.contrib.auth.models import User

def register(request, tournament_id, user_id):
    if request.method == 'POST':
        ourtournament = Tournament.objects.filter(pk=tournament_id).first

        if len(ourtournament.players) != ourtournament.max_of_players: #если можем зарегистрировать
            ouruser = User.objects.filter(pk=user_id).first
            ourplayer = PlayerInTournament()
            ourplayer.player = ouruser
            ourplayer.tournament = ourtournament
            return render("registered_intournament.html")
        else:
            return 0

    else:
        return render(request, "register_intournament.html")
