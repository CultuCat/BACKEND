from django.http import JsonResponse
from subprocess import run

def scr_refresh(request):
    run(['python', 'manage.py', 'runscript', 'refresh'], check=True)
    return JsonResponse({'message': 'Refreshed successfully'})