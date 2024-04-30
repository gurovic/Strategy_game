from django.http import JsonResponse
from django.shortcuts import render
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament


from django.contrib.auth.models import User


def register(request, tournament_id, user_id):
    ourtournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':
        try:
            try_to_get_player = ourtournament.players.get(pk=user_id)
        except:
            try_to_get_player = None

        if try_to_get_player is None and len(
                ourtournament.players.all()) != ourtournament.max_of_players:  # если можем зарегистрировать
            ouruser = User.objects.get(pk=user_id)
            ourtournament.players.add(ouruser)
            return JsonResponse({'status': 'done'}, status=200)
        elif try_to_get_player != None:
            return JsonResponse({'status': 'already registered'}, status=200)
        else:
            return JsonResponse({'status': 'denied registration'})
    else:
        return JsonResponse({'status': 'ok'})
