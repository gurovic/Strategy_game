from django.shortcuts import render
from website.app.models import Tournament


def show(request, id):
    tournament = Tournament.objects.get(pk=id)

    user_links = list(tournament.players.all())
    n_players = len(user_links)
    table = [[0] * n_players for _ in range(n_players)]
    battles = tournament.battles.all()

    user_link_row = dict()
    for i in range(n_players):
        user_link_row[user_links[i]] = i

    user_link_points = dict()
    for i in range(n_players):
        user_link_points[user_links[i]] = 0

    for battle in battles:
        player_in_battle_1 = battle.players[0]
        player_in_battle_2 = battle.players[1]

        table[user_link_row[player_in_battle_1.user]][
            user_link_row[player_in_battle_2.user]] = player_in_battle_1.number_of_points
        table[user_link_row[player_in_battle_2.user]][
            user_link_row[player_in_battle_1.user]] = player_in_battle_2.number_of_points

        user_link_points[player_in_battle_1] += player_in_battle_1.number_of_points
        user_link_points[player_in_battle_2] += player_in_battle_2.number_of_points

    strings = list()
    head = ["place/number", "name", "points"]
    for i in range(n_players):
        head.append(i)
    strings.append(head)
    for i in range(n_players):
        strings.append([[i + 1] + ["name"] + [user_link_points[user_links[i]]] + table[i]]) #change ["name"] to [user_links[i].name]

    strings.sort(key=lambda x: x[2])

    return render(request, 'tournament_status_views.html', {'strings': strings})
