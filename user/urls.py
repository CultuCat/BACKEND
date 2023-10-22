from rest_framework import routers
from . import views
from .views import PerfilView, SignIn_Google
from django.urls import re_path


router = routers.DefaultRouter()

router.register('perfils', PerfilView, 'Perfils')

urlpatterns = router.urls + [re_path('sign_in/(?P<backend>[^/]+)/$', SignIn_Google)]