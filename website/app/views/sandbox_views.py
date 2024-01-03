import time
from django.shortcuts import render

from ..models import CompilerReport, Game
from ..classes import Sandbox, SandboxNotifyReceiver, CompilerNotifyReceiver
from ..compiler import Compiler


def show(request, id):
    if request.method == 'POST':
        print(1)
        file_compiler = CompilerNotifyReceiver(request.FILES['strategy'], request.POST['language'])
        print(2)
        file_compiler.run()
        print(3)
        return {'status': 'subscribe to compiler', 'compiler': file_compiler}
    else:
        return render(request, "sandbox.html", {})
