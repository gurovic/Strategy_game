from django.shortcuts import render
from Strategy_game.website.app.forms import TournamentForm

# Create your views here.

def start_page(request):
    return render(request, 'templates/tournament_page.html')


def create_tounament(request):

    form = TournamentForm()

    data = {
        'form': form
    }

    return render(request, 'templates/tournament_create.html', data)