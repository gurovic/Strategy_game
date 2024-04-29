from app.classes.logger import method_log
from app.models import Tournament
from app.models import PlayerInTournament
from django.http import JsonResponse

def show(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except Tournament.DoesNotExist:
        return JsonResponse({"error": "This tournament does not exist"}, status=404)

    players_in_tournament = PlayerInTournament.objects.filter(tournament=tournament).order_by("-number_of_points")

    data = []
    for player in players_in_tournament:
        player_data = {
            'player_id': player.player_id,
            'tournament_id': player.tournament_id,
            'place': player.place,
            'number_of_points': player.number_of_points,
            'file_solution': player.file_solution.url,
            'player_name': player.player.username
        }
        data.append(player_data)

    return JsonResponse({'tournament': {'id': tournament.id, 'name': tournament.name}, 'playersInTournament': data})
