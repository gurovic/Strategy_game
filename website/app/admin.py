from app.models.compiler_report import CompilerReport
from app.models.model_tournament import Tournament

from django.contrib import admin


@admin.register(CompilerReport)
class CompilerReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass
