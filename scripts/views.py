from django.http import JsonResponse
from subprocess import run
import sys
import os
import subprocess

def scr_refresh(request):
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    python_path = sys.executable

    command = [python_path, os.path.join(project_path, 'manage.py'), 'runscript', 'refresh']
    try:
        run(command, check=True)
    except subprocess.CalledProcessError as e:
        # Manejar el error
        error_message = str(e)
        return JsonResponse({'error': error_message}, status=500)
    return JsonResponse({'message': 'Refreshed successfully'})
