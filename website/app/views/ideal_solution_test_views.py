from ..models.ideal_solution_form import IdealSolutionPostForm
from ..classes.generate_battle import generate_battle, save_file
from ..models.game import Game

from django.shortcuts import render


def show_all(request):
    # return render(request, "compiler_reports_all.html", {"compiler_reports": compiler_reports})
    pass

def show(request, id:int):
    # return render(request, "compiler_reports_all.html", {"compiler_reports": compiler_reports})
    pass

def post_new(request):
    if request.method == 'POST':
        form = IdealSolutionPostForm(request.POST)
        if form.is_valid():
            play = form.play
            solution = form.solution
            solution_filename = save_file(solution)
            play_filename = save_file(play)
            game = Game(play=play_filename, ideal_solution=solution_filename)
            generate_battle(game,solution_filename)
    else:
        form = IdealSolutionPostForm()
        return render(request,'ideal_solution_loader.html', {'form':form})
