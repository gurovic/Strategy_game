from django.shortcuts import render

from app.models import Tournament


def start_tournament(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except:
        return render(request, 'tournament_start.html', {'status': "can't find this tournament in database"})

    if request.method == "POST":
        tournament.start_tournament()
        return render(request, 'tournament_start.html',
                      {'status': 'getting report', 'tournament': tournament})
    return render(request, 'tournament_start.html', {'status': 'posting tournament', 'tournament': tournament})
