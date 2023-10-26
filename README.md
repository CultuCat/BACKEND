#Sonar Status:
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=CultuCat_backend&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=CultuCat_backend)

Per fer migracions:
- py -m manage makemigrations 
- py -m manage migrate

Per fer correr en local:
- py -m manage runserver

Actualitzar requirements:
- py -m pip freeze > requirements.txt
- py -m pip install -r requirements.txt