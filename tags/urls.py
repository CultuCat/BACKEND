from rest_framework import routers
from .views import TagView

router = routers.DefaultRouter()
router.register(r'', TagView, basename='tags')

urlpatterns = router.urls
