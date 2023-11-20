from ..models.game import Game
from ..models import CompilerReport

from ..classes import FileLoader, save_file

from django.shortcuts import render
from django import forms


def compile(file):
    path = save_file(file)
    file_loader = FileLoader(path)
    compiler_report_id = file_loader.get_compiler_report_id()
    compiler_report = CompilerReport.objects.get(pk=compiler_report_id)
    return compiler_report


def post_new(request):
    if request.method == 'POST':
        ideal_solution_report = compile(request.FILES['ideal_solution'])
        play_report = compile(request.FILES['play'])
        if ideal_solution_report.status == 0 and play_report.status == 0:
            game = Game(name=request.POST['name'], number_of_players=request.POST['number_of_players'],
                        ideal_solution=ideal_solution_report.compiled_file, play=play_report.compiled_file)
            game.save()
            return render(request, 'game-post.html', {'feedback': game,
                                                      'ideal_solution_report': ideal_solution_report,
                                                      'play_report': play_report})
        else:
            return render(request, 'game-post.html', {
                'ideal_solution_report': ideal_solution_report,
                'play_report': play_report})
    else:
        return render(request, 'game-post.html', {'game': Game()})
