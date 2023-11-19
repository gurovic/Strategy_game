from ..classes.generate_battle import generate_battle
from ..models.game import Game

from django.shortcuts import render


def post_new(request, id):
    game = Game.objects.get(pk=id)
    if request.method == 'POST':
        report = generate_battle(game)
        return render(request, 'ideal_solution_loader.html', {'report': report, 'game': game})
    else:
        return render(request,'ideal_solution_loader.html', {'game': game})
