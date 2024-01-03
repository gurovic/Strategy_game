import time
from django.shortcuts import render

from ..models import CompilerReport, Game
from ..classes import Sandbox, SandboxNotifyReceiver, CompilerNotifyReceiver
from ..compiler import Compiler


def show(request, id):
    if request.method == 'POST':
        file_compiler = CompilerNotifyReceiver(request.FILES['strategy'], request.POST['language'])
        file_compiler.run()
        strategy = None
        while strategy is None:
            time.sleep(0.1)
            strategy = file_compiler.compiler_report

        if strategy.status == 0:
            game = Game.objects.get(pk=id)
            sandbox = SandboxNotifyReceiver(game, strategy)
            report = sandbox.report()
            while report is None:
                time.sleep(0.1)
                report = sandbox.report()
            return render(request, 'sandbox.html', {'report': report})
        else:
            return render(request, 'sandbox.html', {'failed_report': strategy})
    else:
        return render(request, "sandbox.html", {})
