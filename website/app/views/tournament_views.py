from django.shortcuts import render, redirect
from ..forms import TournamentForm
from ..models.tournament import Tournament
from Strategy_game.website.app.forms import TournamentForm

# Create your views here.

def start_page(request):
    return render(request, 'templates/tournament_page.html')


def create_tounament(request):
    error = ''
    if request.method == "POST":
        form = TournamentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('tounrament_startpage')
        else:
            error = 'Форма заполнена неверно'

    form = TournamentForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'templates/tournament_create.html', data)