from invoker.models import InvokerReport, File

from django.contrib import admin


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(InvokerReport)
class InvokerReportAdmin(admin.ModelAdmin):
    pass
