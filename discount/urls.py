from rest_framework import routers
from . import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'', views.DiscountsView, basename='discounts')

urlpatterns = router.urls