from functools import partial

from django.shortcuts import render, redirect
from django.views import View

from ..compiler import Compiler
from ..game_upload_form import GameForm
from ..models import Game
from website.settings import SUPPORTED_LANGUAGES as LANGUAGES


class GameUploadFormView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'game_upload.html', {
            'status': 'game form',
            'game_form': GameForm,
            'available_languages': LANGUAGES,
        })

    def post(self, request, *args, **kwargs):
        print('herfmsdklfmklsdmkl')
        game_form = GameForm(data=request.POST)

        if game_form.is_valid():
            try:
                if not request.session.get('game_been_uploaded'):
                    Game.objects.get(id=request.session['game_id']).delete()
            except:
                pass

        game_model = Game.objects.create(**game_form.cleaned_data)
        request.session['game_id'] = game_model.id
        ideal_solution = request.FILES.get('ideal_solution')
        game_model.ideal_solution = request.FILES.get('ideal_solution')
        game_model.play = request.FILES.get('play')
        game_model.visualiser = request.FILES.get('visualiser')
        game_model.rules = request.FILES.get('rules')
        game_model.save()

        ideal_solution = Compiler(
            game_model.ideal_solution.path,
            request.POST['ideal_solution_language'],
            callback=partial(self.notify, label='ideal_solution')
        )

        play = Compiler(
            game_model.play.path,
            request.POST['play_language'],
            callback=partial(self.notify, label='play', game_model=game_model)
        )

        visualiser = Compiler(
            game_model.visualiser.path,
            request.POST['visualiser_language'],
            callback=partial(self.notify, label='visualiser')
        )
        request.session['ideal_solution_report_id'] = None
        request.session['play_report_id'] = None
        request.session['visualiser_report_id'] = None

        ideal_solution.compile()
        play.compile()
        visualiser.compile()
        return redirect('game_upload_compilation')

    def notify(self, report, label, game_model=None):
        if label == 'ideal_solution':
            self.request.session['ideal_solution_report_id'] = report.id
        elif label == 'play':
            game_model.compiled_play = report.compiled_file
            game_model.save()
            self.request.session['play_report_id'] = report.id
        elif label == 'visualiser':
            self.request.session['visualiser_report_id'] = report.id
