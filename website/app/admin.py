from django.contrib import admin

from .models import CompilerReport, InvokerReport, Game

# Register your models here.
admin.site.register(CompilerReport)
admin.site.register(InvokerReport)

admin.site.register(Game)
