from rest_framework import routers
from .views import EventView
from django.urls import re_path

router = routers.DefaultRouter()
router.register(r'', EventView, basename='esdeveniments')

urlpatterns = [
    *router.urls,
    re_path('home', EventView.as_view({'get': 'home'}), name='home events'),
    re_path('today', EventView.as_view({'get': 'today'}), name='today events'),
    re_path('this_week', EventView.as_view({'get': 'this_week'}), name='this week events'),
    re_path('free', EventView.as_view({'get': 'free'}), name='free events'),
    re_path('popular', EventView.as_view({'get': 'popular'}), name='popular events'),
]