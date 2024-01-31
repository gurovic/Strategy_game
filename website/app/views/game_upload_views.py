from django.shortcuts import render
from django.views import View
from ..game_upload_form import GameForm
from ..classes import LANGUAGES
from ..compiler import Compiler
from functools import partial


class GameUploadView(View):
    template_name = 'game_upload.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualizer_report = None
        self.play_status = None
        self.play_report = None
        self.ideal_solution_status = None
        self.visualizer_status = None
        self.ideal_solution_report = None
        self.game_form = GameForm()

    def get(self, request, *args, **kwargs):
        print(0)
        return render(request, self.template_name, {
            'status': 'filling compilation form',
            'game_form': self.game_form,
            'available_languages': LANGUAGES,
        })

    def post(self, request, *args, **kwargs):
        if request.POST['type'] == 'compiler':
            self.game_form = GameForm(request.POST)
            ideal_solution = Compiler(
                request.FILES['ideal_solution'],
                LANGUAGES[request.POST['ideal_solution_language']],
                partial(self.notify, 'ideal_solution')
            )
            play = Compiler(
                request.FILES['play'],
                LANGUAGES[request.POST['play_language']],
                partial(self.notify, 'play')
            )
            visualizer = Compiler(
                request.FILES['visualizer'],
                LANGUAGES[request.POST['visualizer_language']],
                partial(self.notify, 'visualizer')
            )
            print(1)
            ideal_solution.compile()
            play.compile()
            visualizer.compile()
            print(2)
            return render(request, self.template_name, {
                'status': 'compilation',
                'game_form': self.game_form,
                'ideal_solution_report': self.ideal_solution_report,
                'play_report': self.play_report,
                'visualizer_report': self.visualizer_report,
            })

        elif request.POST['type'] == 'compilation in progress':
            print(3)
            status = 'compilation'
            if self.ideal_solution_status == self.play_status == self.visualizer_status == 'Done':
                status = 'receive compiler report'

            return render(request, self.template_name, {
                'status': status,
                'game_form': self.game_form,
                'ideal_solution_report': self.ideal_solution_report,
                'play_report': self.play_report,
                'visualizer_report': self.visualizer_report,
            })

    def notify(self, compiler_report, label):
        if label == 'ideal_solution':
            self.ideal_solution_report = compiler_report
            self.ideal_solution_status = 'Done'
        elif label == 'play':
            self.play_report = compiler_report
            self.play_status = 'Done'
        elif label == 'visualizer':
            self.visualizer_report = compiler_report
            self.visualizer_status = 'Done'
