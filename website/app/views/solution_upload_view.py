from django.shortcuts import render
from ..models.tournament import Tournament
from ..models.player_in_tournament import PlayerInTournament

def upload(request, tournament_id, user_id):
    our_tournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':
        current_player_in_tournament = our_tournament.players.get(pk=user_id)
        current_player_in_tournament.file_solution = request.FILES['strategy'].read()
        return render(request, 'solution_upload.html', {'status': 'strategy uploaded'})

    else:
        if our_tournament.Status == 'WAITING_SOLUTIONS':
            return render(request, 'solution_upload.html', {'status': 'wait for strategy'})
        elif our_tournament.Status == 'NOT_STARTED':
            return render(request, 'solution_upload.html', {'status': 'not started'})
        else:
            return render(request, 'solution_upload.html', {'status': 'finished'})

