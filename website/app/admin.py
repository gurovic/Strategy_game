from django.contrib import admin

from .models import CompilerReport,InvokerReport

# Register your models here.
admin.site.register(CompilerReport)
admin.site.register(InvokerReport)
