from django.shortcuts import render, redirect
from django.views import View

from ..models import CompilerReport, Game

class GameUploadReportView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        ideal_solution_status = CompilerReport.objects.get(id=request.session.get('ideal_solution_report_id')).status
        play_status = CompilerReport.objects.get(id=request.session.get('play_report_id')).status
        visualiser_status = CompilerReport.objects.get(id=request.session.get('visualiser_report_id')).status

        request.session['game_can_be_uploaded'] = not (ideal_solution_status or play_status or visualiser_status)

        return render(request, 'game_upload.html', {
            'status': 'receive compiler report',
            'ideal_solution_report': ideal_solution_status,
            'play_report': play_status,
            'visualiser_report': visualiser_status,
            'game_can_be_uploaded': request.session['game_can_be_uploaded']
        })

    def post(self, request, *args, **kwargs):

        if request.POST['type'] == 'game':
            game_model = Game.objects.get(id=request.session.get('game_id'))

            request.session['game_been_uploaded'] = True
            return render(request, 'game_upload.html', {
                'status': 'game uploaded',
                'game_name': game_model.name
            })

        elif request.POST['type'] == 'dont upload':
            Game.objects.get(id=request.session.get('game_id')).delete()

            return redirect('game_upload_form')

        elif request.POST['type'] == 'new game':
            return redirect('game_upload_form')
