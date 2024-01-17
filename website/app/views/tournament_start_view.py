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

        return render(request, 'tournament_start.html', {'status': 'OK', 'tournament': tournament})

    return render(request, 'tournament_start.html', {'status': 'OK', 'tournament': tournament})
