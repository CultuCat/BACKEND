from rest_framework import routers
from .views import EventView
from django.urls import re_path

router = routers.DefaultRouter()
router.register(r'', EventView, basename='esdeveniments')

urlpatterns = [
    *router.urls,
    re_path('home', EventView.as_view({'get': 'home'}), name='home events'),
    re_path('today', EventView.as_view({'get': 'today'}), name='today events'),
]