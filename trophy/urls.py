from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.TrophyView, basename='trophies')

urlpatterns = router.urls