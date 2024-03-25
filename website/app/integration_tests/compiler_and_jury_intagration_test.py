import unittest

from invoker.invoker_request import InvokerRequest
from invoker.invoker_request import InvokerRequestType
from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_multi_request import Priority
from app.classes.jury import GameState
from app.classes.jury import Jury
from app import compiler

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

        compiler1 = compiler.Compiler(play_code, "py", play_compiled.get_compiled_file).compile()
        compiler2 = compiler.Compiler(solution_first_code, "py", solution_first_compiled.get_compiled_file).compile()
        compiler3 = compiler.Compiler(solution_second_code, "py", solution_second_compiled.get_compiled_file).compile()

        while play_compiled.ok + solution_first_compiled.ok + solution_second_compiled.ok != 3:
            continue

        play_compiled_path = "../website/media/" + "/".join(str(play_compiled.compiled_file).split("\\"))
        solution_first_compiled_path = "../website/media/" + "/".join(
            str(solution_first_compiled.compiled_file).split("\\"))
        solution_second_compiled_path = "../website/media/" + "/".join(
            str(solution_second_compiled.compiled_file).split("\\"))

        launcher_play = launcher.Launcher(play_compiled_path)
        launcher_strategy1 = launcher.Launcher(solution_first_compiled_path)
        launcher_strategy2 = launcher.Launcher(solution_second_compiled_path)

        IR_play = InvokerRequest(launcher_play.command(), [play_compiled_path])
        IR_play.label = "play"
        IR_sol1 = InvokerRequest(launcher_strategy1.command(), [solution_first_compiled_path])
        IR_sol1.label = "strategy"
        IR_sol2 = InvokerRequest(launcher_strategy2.command(), [solution_second_compiled_path])
        IR_sol2.label = "strategy"

        IM_process_of_battle = InvokerMultiRequest([IR_play, IR_sol1, IR_sol2], Priority.RED)
        jury_of_battle = Jury(IM_process_of_battle)
        IM_process_of_battle.start()
        self.assertIs(GameState.END, jury_of_battle.game_state)
