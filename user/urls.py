from rest_framework import routers
from . import views
from django.urls import re_path
from .views import PerfilView


router = routers.DefaultRouter()

router.register(r'', PerfilView, 'Perfils')

urlpatterns = [
    *router.urls,
    re_path('loginPerfil', views.loginPerfil),
    re_path('signupPerfil', views.signupPerfil),
    re_path('test_tokenPerfil', views.test_tokenPerfil),
]