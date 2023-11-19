from ..models.game import Game

from django.shortcuts import render


def post_new(request):
    if request.method == 'POST':
        game = Game(name=request.POST['name'], number_of_players=request.POST['number_of_players'],
                    ideal_solution=request.POST['ideal_solution'], play=request.POST['play'])
        game.save()
        return render(request, 'game-post.html', {'feedback': game})
    else:
        return render(request, 'game-post.html', {'game': Game()})
