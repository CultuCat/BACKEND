from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.CommentsView, basename='comments')

urlpatterns = router.urls