Per fer migracions:
- py -m manage makemigrations 
- py -m manage migrate

Per fer correr en local:
- py -m manage runserver

Actualitzar requirements:
- py -m pip freeze > requirements.txt
- py -m pip install -r requirements.txt