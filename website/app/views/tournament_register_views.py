from django.shortcuts import render
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament
from django.contrib.auth.models import User


def register(request, tournament_id, user_id):
    if request.method == 'POST':
        ourtournament = Tournament.objects.filter(pk=tournament_id).first()
        try:
            try_to_get_player = ourtournament.players.get(pk=user_id)
        except:
            try_to_get_player = None

        if try_to_get_player is None and len(
                ourtournament.players.all()) != ourtournament.max_of_players:  # если можем зарегистрировать
            ouruser = User.objects.filter(pk=user_id).first()
            ourplayer = PlayerInTournament.objects.create(player=ouruser, tournament=ourtournament, file_solution=None)
            ourtournament.players.add(ouruser)
            return render(request, 'register_intournament.html', {'status': 'registered'})
        elif try_to_get_player != None:
            return render(request, 'register_intournament.html', {'status': 'already registered'})
        else:
            return render(request, 'register_intournament.html', {'status': 'denied registration'})

    else:
        return render(request, 'register_intournament.html', {'status': 'not registered'})
