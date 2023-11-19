from rest_framework import routers
from . import views
from django.urls import re_path
from .views import PerfilView


router = routers.DefaultRouter()

router.register(r'', PerfilView, 'Perfils')

urlpatterns = [
    *router.urls,
    re_path('login', views.loginPerfil),
    re_path('signup', views.signupPerfil),
]