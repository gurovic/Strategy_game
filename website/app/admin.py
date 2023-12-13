from app.models import CompilerReport
from .models import Tournament

from django.contrib import admin


@admin.register(CompilerReport)
class CompilerReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass
