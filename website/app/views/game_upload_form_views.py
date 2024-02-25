from functools import partial

from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from ..compiler import Compiler
from ..game_upload_form import GameForm
from ..models import CompilerReport, Game
from ..classes.game_upload_middleware import DeleteGameOnExitMiddleware

LANGUAGES = {
    'c++': 'cpp',
    'c#': 'cs',
    'c': 'c',
    'python': 'py',
    'javascript': 'js',
    'java': 'Java',
}


@method_decorator(DeleteGameOnExitMiddleware, name='dispatch')
class GameUploadView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'game_upload_form.html', {
            'status': 'game form',
            'game_form': GameForm,
            'available_languages': LANGUAGES,
        })

    def post(self, request, *args, **kwargs):
        print(request)
        if request.POST['type'] == 'compiler':
            game_form = GameForm(data=request.POST)
            if game_form.is_valid():
                game_model = Game.objects.create(**game_form.cleaned_data)
                game_model.ideal_solution = request.FILES['ideal_solution']
                game_model.play = request.FILES['play']
                game_model.visualiser = request.FILES['visualiser']
                game_model.rules = request.FILES['rules']
                request.session['game_id'] = game_model.id
                game_model.save()

            ideal_solution = Compiler(
                request.FILES['ideal_solution'].read(),
                LANGUAGES[request.POST['ideal_solution_language']],
                partial(self.notify, label='ideal_solution')
            )

            play = Compiler(
                request.FILES['play'].read(),
                LANGUAGES[request.POST['play_language']],
                partial(self.notify, label='play')
            )

            visualiser = Compiler(
                request.FILES['visualiser'].read(),
                LANGUAGES[request.POST['visualiser_language']],
                partial(self.notify, label='visualiser')
            )
            request.session['ideal_solution_report_id'] = None
            request.session['play_report_id'] = None
            request.session['visualiser_report_id'] = None
            ideal_solution.compile()
            play.compile()
            visualiser.compile()
            return render(request, self.template_name, {
                'status': 'compiling',
            })

        elif request.POST['type'] == 'compilation':
            ideal_solution_report = CompilerReport.objects.get(id=request.session['ideal_solution_report_id'])
            play_report = CompilerReport.objects.get(id=request.session['play_report_id'])
            visualiser_report = CompilerReport.objects.get(id=request.session['visualiser_report_id'])
            if ideal_solution_report and play_report and visualiser_report:
                return render(request, self.template_name, {
                    'status': 'receive compiler report',
                    'ideal_solution_report': ideal_solution_report.status,
                    'play_report': play_report.status,
                    'visualiser_report': visualiser_report.status,
                })

            return render(request, self.template_name, {
                'status': 'compiling'
            })

        elif request.POST['type'] == 'game':
            ideal_solution_status = CompilerReport.objects.get(id=request.session['ideal_solution_report_id']).status
            play_status = CompilerReport.objects.get(id=request.session['play_report_id']).status
            visualiser_status = CompilerReport.objects.get(id=request.session['visualiser_report_id']).status
            game_model = Game.objects.get(id=request.session['game_id'])

            if not (ideal_solution_status or play_status or visualiser_status):
                return render(request, self.template_name, {
                    'status':'game downloaded',
                    'game_name':game_model.name})
            else:
                game_model.delete()
                return render(request, self.template_name, {
                    'status':'game form',
                    'game_form': GameForm(),
                    'available_languages': LANGUAGES
                })
        elif request.POST['type'] == 'upload new game':
            return redirect('/app/game_upload/')

    def notify(self, report, label):
        if label == 'ideal_solution':
            self.request.session['ideal_solution_report_id'] = report.id
        elif label == 'play':
            self.request.session['play_report_id'] = report.id
        elif label == 'visualiser':
            self.request.session['visualiser_report_id'] = report.id
