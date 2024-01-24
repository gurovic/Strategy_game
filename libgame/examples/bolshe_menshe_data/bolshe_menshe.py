import libgame


def validate(player_move: libgame.PlayerMove):
    return player_move.data.isnumeric()


def main():

    battle = libgame.get_battle()
    if battle.num_players != 2:
        raise ValueError("Only two user can play!")

    players = {1: 1, 2: 2}
    battle.send_to(1, "your move!")
    player_move1 = battle.wait_for(1)
    if not validate(player_move1):
        battle.set_points(players[2], 1)
        battle.end_due(f"Player {1} made invalid move!")
        return
    battle.send_to(2, f"{int(player_move1.data)}")
    player_move2 = battle.wait_for(2)
    if not validate(player_move2):
        battle.set_points(players[1], 1)
        battle.end_due(f"Player {2} made invalid move!")
        return
    if int(player_move1.data) > int(player_move2.data):
        battle.set_points(players[1], 1)
    elif int(player_move1.data) == int(player_move2.data):
        battle.set_points(players[2], 0.5)
        battle.set_points(players[1], 0.5)
    else:
        battle.set_points(players[2], 1)
    battle.end()


if __name__ == "__main__":
    main()