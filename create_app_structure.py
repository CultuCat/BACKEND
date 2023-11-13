import os

def create_django_app_structure(app_name):
    # Define la ruta base del proyecto
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Crea el directorio de la nueva aplicación
    app_directory = os.path.join(project_root, app_name)
    os.mkdir(app_directory)

    # Crea el archivo __init__.py en la raíz de la aplicación
    open(os.path.join(app_directory, '__init__.py'), 'a').close()

    # Crea los directorios y archivos necesarios en la nueva aplicación
    subdirectories = ['migrations']
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(app_directory, subdirectory)
        os.mkdir(subdirectory_path)
        # Crea el archivo __init__.py en los directorios de migrations 
        open(os.path.join(subdirectory_path, '__init__.py'), 'a').close()

    # Definir importaciones base para cada tipo de archivo
    base_imports = {
        'apps.py': [
            'from django.apps import AppConfig',
        ],
        'admin.py': [
            'from django.contrib import admin',
        ],
        'urls.py': [
            'from rest_framework import routers',
            'from . import views',
        ],
        'models.py': [
            'from django.db import models',
        ],
        'serializers.py': [
            'from rest_framework import serializers',
        ],
        'views.py': [
            'from rest_framework import status',
            'from rest_framework.response import Response',
            'from rest_framework.views import APIView',
        ],
        'tests.py': [
            'from django.test import TestCase',
        ],
    }

    # Crear archivos y agregar importaciones base
    for file_name, imports in base_imports.items():
        file_path = os.path.join(app_directory, file_name)
        with open(file_path, 'a') as file:
            for import_statement in imports:
                file.write(import_statement + '\n')

if __name__ == '__main__':
    app_name = input("Nombre de la nueva aplicación: ")
    create_django_app_structure(app_name)
    print(f"La estructura completa de la aplicación '{app_name}' ha sido creada.")