from django.shortcuts import render

from app.models import Tournament


def start_tournament(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except:
        return render(request, 'tournament_start.html', {'status': 'failed'})

    if request.method == "POST":
        tournament.end()
        # we get the current result of the battle and return it to display in the html part
        left_battles = tournament.system.battle_count
        players = tournament.players.objects.all()
        players.sort(key=lambda x: x.score, reverse=True)
        return_players = []
        for i in range(len(players)):
            return_players.append({'place': i, 'score': players[i].score, 'name': players[i].player})
        return render(request, 'tournament_start.html',
                      {'status': 'getting report', 'tournament': tournament, 'left_battles': left_battles,
                       'players': return_players})
    return render(request, 'tournament_start.html', {'status': 'posting tournament', 'tournament': tournament})
