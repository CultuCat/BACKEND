from rest_framework import routers
from . import views
from django.urls import path
from .views import MessageAPIView

urlpatterns = [
    path('messages', MessageAPIView.as_view())
]


# router = routers.DefaultRouter()
# router.register(r'', views.MessagesView, basename='messages')

# urlpatterns = router.urls