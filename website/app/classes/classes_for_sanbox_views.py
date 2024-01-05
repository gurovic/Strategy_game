from ..compiler import Compiler
from ..models import CompilerReport
from .sandbox import Sandbox

LANGUAGES = {
    'c++': 'cpp',
    'c#': 'cs',
    'c': 'c',
    'python': 'py',
    'javascript': 'js',
    'java': 'Java',
}


class CompilerNotifyReceiver:
    def __init__(self, file, lang):
        self.report = None
        self.compiler_report = None
        self.file = file
        self.lang = LANGUAGES[lang]
        self.compiler = Compiler(self.file, self.lang, self.notify)

    def run(self):
        self.compiler.compile()

    def notify(self, report):
        self.report = report


class SandboxNotifyReceiver:
    def __init__(self, game, strategy):
        self.report = None
        self.game = game
        self.strategy = strategy
        self.sandbox = Sandbox(game, strategy, self.notify)

    def run(self):
        self.sandbox.run_battle()

    def notify(self, report):
        self.report = report
