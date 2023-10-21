from rest_framework import routers
from . import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'', views.TicketsView, basename='tickets')

urlpatterns = router.urls