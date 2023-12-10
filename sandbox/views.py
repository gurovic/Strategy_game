from django.shortcuts import render
from Strategy_game.sandbox.models.sandbox import Sandbox
from Strategy_game.sandbox.forms import SandboxForm


def run_sandboxForm(request):
    form=SandboxForm()#создали экземпляр
    return render(request, 'sandbox/sandboxform.html', {'form': form})

def run_sandbox(request, id):
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
