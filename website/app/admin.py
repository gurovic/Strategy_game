from .models import CompilerReport, Tournament, Game

from django.contrib import admin


admin.site.register(CompilerReport)
admin.site.register(Game)
admin.site.register(Tournament)
