import unittest

from invoker.invoker import NormalProcess
from invoker.invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue
from invoker.invoker_request import InvokerRequest
from invoker.invoker_request import InvokerRequestType
from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_multi_request import Priority
from app.classes.jury import GameState
from app.classes.jury import Jury
from app import compiler
import subprocess

from app import launcher


class Test(unittest.TestCase):
    def test_game_state(self):
        class CompiledFile:
            self.ok = 0

            def get_compiled_file(self, compiler_report):
                self.compiled_file = compiler_report.compiled_file
                self.ok = 1

        play_code = "../libgame/examples/bolshe_menshe_data/bolshe_menshe.py"
        solution_first_code = "../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution1.py"
        solution_second_code = "../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution2.py"

        play_compiled = CompiledFile()
        solution_first_compiled = CompiledFile()
        solution_second_compiled = CompiledFile()

        compiler.Compiler(play_code, "py", play_compiled.get_compiled_file).compile()
        compiler.Compiler(solution_first_code, "py", solution_first_compiled.get_compiled_file).compile()
        compiler.Compiler(solution_second_code, "py", solution_second_compiled.get_compiled_file).compile()

        while play_compiled.ok + solution_first_compiled.ok + solution_second_compiled.ok != 3:
            continue

        play_compiled_path = play_compiled.compiled_file.path
        solution_first_compiled_path = solution_first_compiled.compiled_file.path
        solution_second_compiled_path = solution_second_compiled.compiled_file.path

        launcher_play = launcher.Launcher(play_compiled_path)
        launcher_strategy1 = launcher.Launcher(solution_first_compiled_path)
        launcher_strategy2 = launcher.Launcher(solution_second_compiled_path)

        subprocess_play = subprocess.Popen([launcher_play.command(), play_compiled_path])
        subprocess_strategy1 = subprocess.Popen([launcher_strategy1.command(), solution_first_compiled_path])
        subprocess_strategy2 = subprocess.Popen([launcher_strategy2.command(), solution_second_compiled_path])

        play_process = NormalProcess(subprocess_play, label="play")
        strategy_process_1 = NormalProcess(subprocess_strategy1, label="player1")
        strategy_process_2 = NormalProcess(subprocess_strategy2, label="player2")

        IR_play = InvokerRequest(launcher_play.command(), [play_compiled_path], process_callback=play_process)
        IR_play.label = "play"
        IR_sol1 = InvokerRequest(launcher_strategy1.command(), [solution_first_compiled_path],
                                 process_callback=strategy_process_1)
        IR_sol1.label = "strategy"
        IR_sol2 = InvokerRequest(launcher_strategy2.command(), [solution_second_compiled_path],
                                 process_callback=strategy_process_2)
        IR_sol2.label = "strategy"

        IM_process_of_battle = InvokerMultiRequest([IR_play, IR_sol1, IR_sol2], Priority.RED)
        jury_of_battle = Jury(IM_process_of_battle)

        IM_process_of_battle.subscribe(jury_of_battle)
        IM_process_of_battle.send_process()

        jury_of_battle.perform_play_command()

        self.assertEqual(jury_of_battle.game_state, GameState.PLAY)