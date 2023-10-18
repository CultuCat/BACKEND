from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:event_id>/ticket/', views.TicketDetailView.as_view(), name='event-ticket'),
]
