from ..models.players_in_battle import PlayersInBattle

from django.shortcuts import render


def show(request, id):
    # TODO нам нужно взять из таблицы с COMPILE_REPORT нужный COMPILE_REPORT и вывести его на HTML-страницу
    compiler_report = None
    while True:
        try:
            compiler_report = CompilerReport.objects.get(pk=id)
            break
        except ():
            pass
    return render(request, "compiler_report_details.html", {"compiler_report": compiler_report})

def show_all(request):
    compiler_reports = CompilerReport.objects.all()
    return render(request, "compiler_reports_all.html", {"compiler_reports": compiler_reports})
