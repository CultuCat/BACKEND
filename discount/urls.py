from django.urls import path
from . import views

urlpatterns = [
    path('verificar-descuento/', views.DescuentoView.as_view(), name='verificar_descuento'),
]