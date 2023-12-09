from rest_framework import routers
from .views import MessageViewSet

router = routers.DefaultRouter()
router.register(r'', MessageViewSet, basename='messages')

urlpatterns = router.urls