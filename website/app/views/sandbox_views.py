import time
import csv
from django.shortcuts import render
import os.path
from pathlib import Path

from ..models import CompilerReport, Game
from ..classes import Sandbox, SandboxNotifyReceiver
from ..compiler import Compiler

LANGUAGES = {
    'c++': 'cpp',
    'c#': 'cs',
    'c': 'c',
    'python': 'py',
    'javascript': 'js',
    'java': 'Java',
}


def show(request, game_id):
    game = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        if request.POST['type'] == 'compiler':
            file_content = request.FILES['strategy'].read()
            DIR = Path(__file__).resolve().parent.parent.parent
            name_of_file = "sand_strategy"
            complete_name = os.path.join(DIR / "media", name_of_file + ".py")
            file1 = open(complete_name, "w")
            file1.write(str(file_content.decode()))
            file1.close()
            lang = request.POST['language']
            file_compiler = Compiler(str(DIR / "media/sand_strategy.py"), LANGUAGES[lang], None)
            file_compiler.compile()
            os.remove(str(DIR / "media/sand_strategy.py"))

            return render(request, 'sandbox.html',
                          {'status': 'receive compiler report', 'report': file_compiler.report, 'game': game})
        elif request.POST['type'] == 'sandbox':
            compiler_report_id = request.POST['compiler_report_id']
            compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
            sandbox = SandboxNotifyReceiver(game, compiler_report.compiled_file)

            try:
                # report = {}
                # sandbox.notify(report)
                sandbox.run()
            except ():
                return render(request, 'sandbox.html', {'status': 'none'})

            return render(request, 'sandbox.html',
                          {'status': 'receive sandbox report', 'game': game, 'report': sandbox.report})
        else:
            return render(request, 'sandbox.html', {'status': 'failed', 'game': game})
    else:
        return render(request, "sandbox.html",
                      {'status': 'filling compilation form', 'game': game, 'available_languages': LANGUAGES})
