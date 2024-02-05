from app import compiler
from invoker.invoker_request import InvokerRequest
from invoker.invoker_request import InvokerRequestType
from invoker.invoker_multi_request import InvokerMultiRequest
from invoker.invoker_multi_request import Priority
from app.classes.jury import Jury
from app.classes.jury import GameState
import unittest


class Test(unittest.TestCase):
    def test_game_state(self):
        class CompiledFile:
            def get_compiled_file(self, compiler_report):
                self.compiled_file = compiler_report.compiled_file

        play_code = open("../libgame/examples/bolshe_menshe_data/bolshe_menshe.py").read()
        solution_first_code = open("../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution1.py").read()
        solution_second_code = open("../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution2.py").read()
        play_compiled = CompiledFile()
        solution_first_compiled = CompiledFile()
        solution_second_compiled = CompiledFile()
        compiler1 = compiler.Compiler(play_code, "py", play_compiled.get_compiled_file).compile()
        compiler2 = compiler.Compiler(play_code, "py", solution_first_compiled.get_compiled_file).compile()
        compiler3 = compiler.Compiler(play_code, "py", solution_second_compiled.get_compiled_file).compile()
        play_compiled_path = play_compiled.compiled_file
        solution_first_compiled_path = solution_first_compiled.compiled_file
        solution_second_compiled_path = solution_second_compiled.compiled_file
        IR_play = InvokerRequest("start", play_compiled_path)
        IR_play.type = InvokerRequestType.PLAY
        IR_sol1 = InvokerRequest("start", solution_first_compiled_path)
        IR_sol1.type = InvokerRequestType.STRATEGY
        IR_sol2 = InvokerRequest("start", solution_second_compiled_path)
        IR_sol2.type = InvokerRequestType.STRATEGY
        IM_process_of_battle = InvokerMultiRequest([IR_play, IR_sol1, IR_sol2], Priority.RED)
        jury_of_battle = Jury(IM_process_of_battle).perform_play_command()
        self.assertIs(GameState.END, jury_of_battle.game_state)








