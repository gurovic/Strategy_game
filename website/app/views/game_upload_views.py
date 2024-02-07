from functools import partial

from django.shortcuts import render
from django.views import View

from ..compiler import Compiler
from ..game_upload_form import GameForm

LANGUAGES = {
    'c++': 'cpp',
    'c#': 'cs',
    'c': 'c',
    'python': 'py',
    'javascript': 'js',
    'java': 'Java',
}


class GameUploadView(View):
    template_name = 'game_upload.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualizer = None
        self.play = None
        self.ideal_solution = None
        self.play_report = None
        self.visualizer_report = None
        self.ideal_solution_report = None
        self.game_form = GameForm()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'status': 'compilation form',
            'game_form': self.game_form,
            'available_languages': LANGUAGES,
        })

    def post(self, request, *args, **kwargs):
        print(request.POST['type'])
        if request.POST['type'] == 'compiler':
            self.game_form = GameForm(request.POST)
            self.ideal_solution = Compiler(
                request.FILES['ideal_solution'].read(),
                LANGUAGES[request.POST['ideal_solution_language']],
                partial(self.notify, label='ideal_solution')
            )

            self.play = Compiler(
                request.FILES['play'].read(),
                LANGUAGES[request.POST['play_language']],
                partial(self.notify, label='play')
            )

            self.visualizer = Compiler(
                request.FILES['visualizer'].read(),
                LANGUAGES[request.POST['visualizer_language']],
                partial(self.notify, label='visualizer')
            )
            self.ideal_solution.compile()
            self.play.compile()
            self.visualizer.compile()
            print(self.ideal_solution)
            print(self.play_report)
            return render(request, self.template_name, {
                'status': 'compiling',
                'game_form': self.game_form,
                'ideal_solution_report': self.ideal_solution.report,
                'play_report': self.play.report,
                'visualizer_report': self.visualizer.report,
            })

        elif request.POST['type'] == 'compilation':
            status = 'compiling'
            if self.ideal_solution_report and self.play_report and self.visualizer_report:
                status = 'receive compiler report'

            print(self.ideal_solution)
            print(self.play_report)
            return render(request, self.template_name, {
                'status': status,
                'game_form': self.game_form,
                'ideal_solution_report': self.ideal_solution_report,
                'play_report': self.play_report,
                'visualizer_report': self.visualizer_report,
            })

    def notify(self, report, label):
        if label == 'ideal_solution':
            self.ideal_solution_report = report
        elif label == 'play':
            self.play_report = report
        elif label == 'visualizer':
            self.visualizer_report = report
