from django.shortcuts import render
from ..models import Tournament, PlayerInTournament
from django.contrib.auth.models import User

def register(request, tournament_id, user_id):
    if request.method == 'POST':
        ourtournament = Tournament.objects.filter(pk=tournament_id).first

        if len(ourtournament.players) != ourtournament.max_of_players: #если можем зарегистрировать
            ouruser = User.objects.filter(pk=user_id).first
            ourplayer = PlayerInTournament.objects.create()
            ourplayer.player = ouruser
            ourplayer.tournament = ourtournament
            ourplayer.file_solution = 0
            ourplayer.save()
            return render("registered_intournament.html", {'status': 'registered'})
        else:
            return render("registered_intournament.html", {'status': 'denied registration'})

    else:
        return render(request, "register_intournament.html", {'status': 'not registered'})
