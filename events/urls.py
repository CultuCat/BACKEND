from rest_framework import routers
from .views import EventView

router = routers.DefaultRouter()
router.register(r'', EventView, basename='esdeveniments')

urlpatterns = router.urls