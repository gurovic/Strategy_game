from django.http import JsonResponse
from django.shortcuts import render
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament


def upload(request, tournament_id, user_id):
    our_tournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':
        current_player_in_tournament = our_tournament.players.get(pk=user_id)
        current_player_in_tournament.file_solution = request.POST['strategy']
        return JsonResponse({'ok': True}, status=200)
    else:
        if our_tournament.Status == 'WAITING_SOLUTIONS':
            return JsonResponse({'ok': False}, status=206)
        elif our_tournament.Status == 'NOT_STARTED':
            return JsonResponse({'ok': False}, status=206)
        else:
            return JsonResponse({'ok': False}, status=206)

