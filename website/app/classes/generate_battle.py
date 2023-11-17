import datetime
import random

from ..models.game import Game
from .battle import Battle
from ..models.players_in_battle import PlayersInBattle
from ..models.battle_report import BattleReport


def generate_filename():
    date = datetime.datetime.now()
    id = random.randint(1,1000000000000)
    return "file"+str(date)+str(id)


def save_file(new_file):
    filename = generate_filename()
    file = open(filename, 'wb')
    file.write(new_file.content)
    file.close()
    return filename


def generate_battle(game:Game):
    players = []
    for i in range(game.number_of_players):
        players.append(PlayersInBattle(game.ideal_solution, i))
    battle = Battle(game, players)
    battle.run()
    report = battle.get_report()
    battle_report = BattleReport(invoker_report=report, battle_id=battle.id)
    return report
