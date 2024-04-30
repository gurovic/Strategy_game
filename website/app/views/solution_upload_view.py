from django.http import JsonResponse
from django.shortcuts import render
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament

def upload(request, tournament_id, user_id):
    our_tournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':
        current_player_in_tournament = PlayerInTournament.objects.get(player__id=user_id, tournament__id=tournament_id)
        current_player_in_tournament.file_solution = request.FILES['strategy']
        current_player_in_tournament.save()
        return JsonResponse({'status': 'strategy uploaded'})

    else:
        if our_tournament.status == Tournament.Status.WAITING_SOLUTIONS:
            return JsonResponse({'status': 'wait for strategy'})
        elif our_tournament.status == Tournament.Status.NOT_STARTED:
            return JsonResponse({'status': 'not started'})
        else:
            return JsonResponse({'status': 'finished'})
