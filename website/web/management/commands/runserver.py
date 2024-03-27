import atexit
import os
import platform
import subprocess
import sys

from django.core.management.commands.runserver import Command as BaseRunserverCommand
from django.conf import settings

_ALREADY_WATCHING = False

_SHELL = platform.system() == "Windows"


def _safe_kill(p):
    try:
        p.terminate()
        p.wait(5)
    except:
        pass
    try:
        p.kill()
    except:
        pass


class Command(BaseRunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--watch', action='store_true', dest='watch', help='Runs JS build in development mode')
        parser.add_argument('--django-q', action='store_true', dest='django_q', help='Runs DjangoQ')
        parser.add_argument('--log', action='store_true', dest='log', help='Log processes')
        parser.add_argument('--internal-run', action='store_true', dest='internal_run',
                            help='This starts the actual server')

    def handle(self, *args, **options):
        if not options['internal_run']:
            if options['watch']:
                self.watch_js(options['log'])
            if options['django_q']:
                self.run_django_q(options['log'])
        super().handle(*args, **options)

    def watch_js(self, log_build: bool = False):
        global _ALREADY_WATCHING
        if _ALREADY_WATCHING or os.environ.get('RUN_MAIN') == 'true':
            return
        print('Will watch JS ' + repr(self))
        p = subprocess.Popen(['ng', 'build', '--watch', '--output-path', settings.BASE_DIR / "staticfiles" / "angular"],
                             stdout=subprocess.DEVNULL if not log_build else None,
                             stderr=subprocess.STDOUT if not log_build else None, shell=_SHELL,
                             cwd=settings.BASE_DIR / "frontend")
        atexit.register(lambda: _safe_kill(p))
        _ALREADY_WATCHING = True

    def run_django_q(self, log: bool = False):
        if os.environ.get('RUN_MAIN') == 'true':
            return
        p = subprocess.Popen([sys.executable, 'manage.py', 'qcluster'],
                             stdout=subprocess.DEVNULL if not log else None,
                             stderr=subprocess.STDOUT if not log else None, shell=_SHELL,
                             cwd=settings.BASE_DIR)
        atexit.register(lambda: _safe_kill(p))

    # Runs this command but with --internal-run
    def run_child(self, second=False):
        add_args = ['--skip-checks']
        # with shell=False it does NOT interrupt as intended
        c = subprocess.Popen([sys.executable] + sys.argv + ['--internal-run', '--noreload'] + add_args, shell=_SHELL)
        return c
