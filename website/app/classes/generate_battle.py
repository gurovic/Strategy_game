from .battle import Battle
from ..models.players_in_battle import PlayersInBattle
from .file_loader import FileLoader
from ..models.compiler import CompilerReport
from ..models.battle_report import BattleReport


def generate_filename():
    return ""


def save_file(new_file):
    filename = generate_filename()
    file = open(filename, 'wb')
    file.write(new_file.content)
    file.close()
    return filename


def generate_battle(play, ideal_solution: str):
    file_loader = FileLoader(ideal_solution)
    compiler_report_id = file_loader.get_compiler_report_id()
    compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
    compiled_file = compiler_report.compiled_file
    filename = save_file(compiled_file)
    players = [
        PlayersInBattle(path=filename, strategy_id=0),
        PlayersInBattle(path=filename, strategy_id=1),
    ]
    battle = Battle(play, players)
    battle.run()
    report = battle.get_report()
    battle_report = BattleReport(invoker_report=report, battle_id=battle.id)
    return report
