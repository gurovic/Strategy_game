import datetime
import random

from ..models.game import Game
from .battle import Battle
from ..models.players_in_battle import PlayersInBattle
from ..models.battle_report import BattleReport


def generate_filename(file_format: str):
    date = datetime.datetime.now()
    id = random.randint(1, 1000000000000)
    return "file_" + str(date) + "_" + str(
        id) + "." + file_format  # TODO make right directory


def get_format(file):
    return 'cpp'  # TODO


def save_file(new_file):
    file_format = get_format(new_file)
    filename = generate_filename(file_format)
    with open(filename, 'wb+') as destination:
        for chunk in new_file.chunks():
            destination.write(chunk)
    return filename


def generate_battle(game: Game):
    players = []
    for i in range(game.number_of_players):
        players.append(PlayersInBattle(game.ideal_solution, i))
    battle = Battle(game, players)
    battle.run()
    report = battle.get_report()
    battle_report = BattleReport(invoker_report=report, battle_id=battle.id)
    return report
