from django.shortcuts import render
from django.http import HttpResponse
from .forms import TournamentForm

# Create your views here.

def start_page(request):
    return render(request, 'tournament/tournament_page.html')


def create_tounament(request):

    form = TournamentForm()

    data = {
        'form': form
    }

    return render(request, 'tournament/tournament_create.html', data)