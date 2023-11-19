from app.models import CompilerReport

from django.contrib import admin


@admin.register(CompilerReport)
class CompilerReportAdmin(admin.ModelAdmin):
    pass
