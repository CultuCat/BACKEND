from rest_framework import routers
from .views import MessageAPIView

router = routers.DefaultRouter()
router.register(r'', MessageAPIView, basename='esdeveniments')

urlpatterns = router.urls