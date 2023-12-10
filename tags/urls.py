from rest_framework import routers
<<<<<<< Updated upstream
from .views import TagView

router = routers.DefaultRouter()
router.register(r'', TagView, basename='tags')

urlpatterns = router.urls
=======
from . import views
>>>>>>> Stashed changes
