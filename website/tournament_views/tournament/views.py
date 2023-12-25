from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def start_page(request):
    return render(request, 'tournament/tournament_page.html')


def create_tounament(request):
    return render(request, 'tournament/tournament_create.html')