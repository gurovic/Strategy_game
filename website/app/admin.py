from app.models import CompilerReport

from django.contrib import admin
from app.models import CompilerReport, Game
from invoker.models import InvokerReport


@admin.register(CompilerReport)
class CompilerReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(InvokerReport)
admin.site.register(Game)
