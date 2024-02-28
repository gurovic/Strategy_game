from django.shortcuts import render, redirect
from django.views import View

from ..models import CompilerReport


class GameUploadCompilationView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        try:
            ideal_solution_report = CompilerReport.objects.get(id=request.session.get('ideal_solution_report_id'))
            play_report = CompilerReport.objects.get(id=request.session.get('play_report_id'))
            visualiser_report = CompilerReport.objects.get(id=request.session.get('visualiser_report_id'))

            if ideal_solution_report and play_report and visualiser_report:
                return redirect('game_upload_report')

        except:
            pass

        return render(request, 'game_upload.html', {
            'status': 'compiling'
        })
