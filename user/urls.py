from rest_framework import routers
from . import views
from .views import PerfilView, SignIn_Google, TicketUsersView
from django.urls import re_path


router = routers.DefaultRouter()

router.register(r'', PerfilView, 'Perfils')

urlpatterns = [
    *router.urls,
    re_path('sign_in/(?P<backend>[^/]+)/$', SignIn_Google),
    re_path('tickets/<int:event_id>/users/', TicketUsersView.as_view({'get': 'list'}), name='ticket-users-list'),
]