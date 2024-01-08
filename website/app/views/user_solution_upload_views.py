from django.shortcuts import render


def upload(request, tournament_link, user):
    if request.method == 'POST':
        current_player_in_tournament = tournament_link.players[user]
        current_player_in_tournament.file_solution = request.FILES['strategy']
        return render(request, 'successful_user_solution.html')
    else:
        return render(request)
