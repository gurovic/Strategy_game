from django.contrib import admin

from .models import Battle
from .models import Tournament
from .models import Game

admin.site.register(Battle)
admin.site.register(Tournament)
admin.site.register(Game)
