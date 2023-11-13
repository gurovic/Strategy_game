from ..models.boris import FileLoader
from ..models.boris import CompilerReport

from django.shortcuts import render
from django.http import Http404


def show(request, id):
    # TODO нам нужно взять из таблицы с COMPILE_REPORT нужный COMPILE_REPORT и вывести его на HTML-страницу
    while True:
        try:
            compile_report = CompilerReport.objects.get(pk=id)
            break
        except ():
            pass
    return render(request, "models/boris.html", {"compile_report": compile_report})
