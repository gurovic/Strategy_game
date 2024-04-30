from django.core import serializers
from app.models import Game
from django.http import JsonResponse
import ast


def get_by_id(request, game_id: int):
    game = Game.objects.get(pk=game_id)
    serialized_game = serializers.serialize('json', [game])
    serialized_game = ast.literal_eval(serialized_game)[0]
    serialized_game['fields']['id'] = serialized_game['pk']
    serialized_game = serialized_game['fields']
    with open(f'media/{serialized_game["rules"]}', 'r') as file:
        serialized_game['rules'] = file.read()
    return JsonResponse({'game': serialized_game}, status=200)
