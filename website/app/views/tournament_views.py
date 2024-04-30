from django.http import JsonResponse
from django.shortcuts import render, redirect
from ..forms import TournamentForm
from ..models.tournament import Tournament

# Create your views here.
from django.shortcuts import render
from ..models.sandbox import Sandbox
from ..models.game import Game
from ..sandbox_forms import SandboxForm


def run_SandboxForm(request):
    form = SandboxForm()  # создали экземпляр
    return render(request, 'sandbox/sandboxform.html', {'form': form})


def run_Sandbox(request, id):
    if request.method == 'POST':
        strategy = get_compiler_report(request.FILES['strategy'])
        if strategy.status == 0:
            game = Game.objects.get(pk=id)
            sandbox = Sandbox(game, strategy)
            report = sandbox.get_report()
            return render(request, 'sandbox_views.html', {'report': report})
        else:
            return render(request, 'sandbox_views.html', {'failed_report': strategy})
    else:
        return render(request, "sandbox_views.html", {})


# Create your views here.

def start_page(request):
    return render(request, 'tournament_page.html')


def create_tournament(request):
    error = ''
    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tournament_startpage')
        else:
            error = 'Форма заполнена неверно'
    form = TournamentForm()
    data = {
        'form': form,
        'error': error
    }

    return render(request, 'tournament_create.html', data)


def is_registered(request, tournament_id, user_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    try:
        current_player_in_tournament = tournament.players.get(pk=user_id)
        return JsonResponse({'ok': 'ok'}, status=200)
    except:
        return JsonResponse({'ok': 'no'}, status=200)
