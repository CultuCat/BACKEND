from rest_framework import routers
from .views import MessageAPIView
from django.urls import path

urlpatterns = [
    path(r'', MessageAPIView.as_view())
]

# router = routers.DefaultRouter()
# router.register(r'', MessageAPIView, basename='messages')

# urlpatterns = router.urls