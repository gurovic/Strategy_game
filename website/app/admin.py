from .models import CompilerReport
from .models import Tournament
#from .sandbox_forms import SandboxForm

from django.contrib import admin


admin.register(CompilerReport)
#admin.site.register(SandboxForm)
admin.register(Tournament)
