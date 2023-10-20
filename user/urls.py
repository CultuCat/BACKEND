from rest_framework import routers
from . import views
from .views import PerfilView


router = routers.DefaultRouter()

router.register('perfils', PerfilView, 'Perfils')

urlpatterns = router.urls