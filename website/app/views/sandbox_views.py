from ..models.game import Game
from ..models import CompilerReport
from ..classes import FileLoader, save_file, Sandbox

from django.shortcuts import render


def compile(file):
    path = save_file(file)
    file_loader = FileLoader(path)
    compiler_report_id = file_loader.get_compiler_report_id()
    compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
    return compiler_report


def show(request, id):
    if request.method == 'POST':
        strategy = compile(request.FILES['strategy'])
        game = Game.objects.get(pk=id)
        sandbox = Sandbox(game, strategy)
        report = sandbox.get_report()
        return render(request, "sandbox_views.html", {"report": report})
    else:
        return render(request, 'sandbox_views.html', {})
