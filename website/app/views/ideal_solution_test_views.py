from ..classes.generate_battle import generate_battle, save_file
from ..models.game import Game

from django.shortcuts import render


def show_all(request):
    # return render(request, "compiler_reports_all.html", {"compiler_reports": compiler_reports})
    pass

def show(request, id:int):
    # return render(request, "compiler_reports_all.html", {"compiler_reports": compiler_reports})
    pass

def post_new(request, id):
    game = Game.objects.get(pk=id)
    if request.method == 'POST':
        report = generate_battle(game)
        return render(request, 'ideal_solution_loader.html', {'report': report, 'game': game})
    else:
        form = IdealSolutionPostForm()
        return render(request,'ideal_solution_loader.html', {'form':form, 'game':game})
