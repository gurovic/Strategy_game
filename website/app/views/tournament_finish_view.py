from django.shortcuts import render

from app.models.tournament import Tournament


def finish_tournament(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except:
        return render(request, 'tournament_finish.html', {'status': "can't find this tournament in database"})

    if request.method == "POST":
        tournament.end_registration()
        return render(request, 'tournament_finish.html',
                      {'status': 'getting report', 'tournament': tournament})
    return render(request, 'tournament_finish.html', {'status': 'posting tournament', 'tournament': tournament})
