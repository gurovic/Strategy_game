import time
import csv
from django.shortcuts import render

from ..models import CompilerReport, Game
from ..classes import Sandbox, SandboxNotifyReceiver, CompilerNotifyReceiver
from ..compiler import Compiler

TYPE = 'test'


def show(request, game_id):
    game = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        if request.POST['type'] == 'compiler':
            file_object = request.FILES['strategy']
            lang = request.POST['language']
            file_compiler = CompilerNotifyReceiver(file_object, lang)

            if TYPE == 'test':
                report = CompilerReport.objects.create(
                    compiled_file=file_object,
                    status=CompilerReport.Status.OK,
                )
                file_compiler.notify(report)
            else:
                file_compiler.run()

            return render(request, 'sandbox.html',
                          {'status': 'receive compiler report', 'compiler_report': file_compiler.report, 'game': game})
        elif request.POST['type'] == 'sandbox':
            compiler_report_id = request.POST['compiler_report_id']
            compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
            game = Game.objects.get(pk=game_id)
            sandbox = SandboxNotifyReceiver(game, compiler_report.compiled_file)

            if TYPE == 'test':
                report = {}
                sandbox.notify(report)
            else:
                sandbox.run()

            return render(request, 'sandbox.html',
                          {'status': 'subscribe to sandbox', 'game': game, 'sandbox_report': sandbox.report})
        else:
            return render(request, 'sandbox.html', {'status': 'failed', 'game': game})
    else:
        return render(request, "sandbox.html", {'status': 'filling compilation form', 'game': game})
