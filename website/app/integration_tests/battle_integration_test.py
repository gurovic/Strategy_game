from django.test import TestCase

from ..classes.jury import Jury
from ..models import Battle
from ...invoker.invoker_multi_request import InvokerMultiRequest, Priority
from ...invoker.invoker_request import InvokerRequest, InvokerRequestType
from ..compiler import Compiler


class BattleTest(TestCase):
    def BattleRunTest(self):
        battle = Battle()

        class CompiledFile:
            def get_compiled_file(self, compiler_report):
                self.compiled_file = compiler_report.compiled_file

        play_code = "../libgame/examples/bolshe_menshe_data/bolshe_menshe.py"
        solution_first_code = "../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution1.py"
        solution_second_code = "../libgame/examples/bolshe_menshe_data/bolshe_menshe_solution2.py"

        play_compiled = CompiledFile()
        solution_first_compiled = CompiledFile()
        solution_second_compiled = CompiledFile()

        compiler1 = Compiler(play_code, "py", play_compiled.get_compiled_file).compile()
        compiler2 = Compiler(solution_first_code, "py", solution_first_compiled.get_compiled_file).compile()
        compiler3 = Compiler(solution_second_code, "py", solution_second_compiled.get_compiled_file).compile()

        play_compiled_path = play_compiled.compiled_file
        solution_first_compiled_path = solution_first_compiled.compiled_file
        solution_second_compiled_path = solution_second_compiled.compiled_file

        IR_play = InvokerRequest("start", play_compiled_path)
        IR_play.type = InvokerRequestType.PLAY
        IR_sol1 = InvokerRequest("start", solution_first_compiled_path)
        IR_sol1.type = InvokerRequestType.STRATEGY
        IR_sol2 = InvokerRequest("start", solution_second_compiled_path)
        IR_sol2.type = InvokerRequestType.STRATEGY

        IMR = InvokerMultiRequest([IR_play, IR_sol1, IR_sol2], Priority.GREEN)
        jury = Jury(IMR)

        self.assertEqual(battle.status, battle.GameStateChoices.NS)
        battle.run(jury)
        self.assertEqual(battle.status, battle.GameStateChoices.OK)
