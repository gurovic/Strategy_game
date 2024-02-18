from django.contrib import admin

from invoker.models import InvokerReport, File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(InvokerReport)
class InvokerReportAdmin(admin.ModelAdmin):
    pass
