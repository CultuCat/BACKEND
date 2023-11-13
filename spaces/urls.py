from rest_framework import routers
from .views import SpaceView

router = routers.DefaultRouter()
router.register(r'', SpaceView, basename='espais')

urlpatterns = router.urls