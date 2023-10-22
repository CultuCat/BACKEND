from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Space
from .serializers import SpaceSerializer
from django.db.models import F
from django.db.models import FloatField
from django.db.models import ExpressionWrapper
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Func
from django.db.models import Value
from django.db.models.functions import Sqrt, Sin, Cos, Radians

class SpaceFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        latitud = request.query_params.get('latitud')
        longitud = request.query_params.get('longitud')
        distancia_km = request.query_params.get('distancia')

        if latitud and longitud and distancia_km:
            latitud = float(latitud)
            longitud = float(longitud)
            distancia_km = float(distancia_km)

            # Convertir la distancia en kilómetros a grados utilizando la fórmula de Haversine
            earth_radius = 6378  # Radio medio de la Tierra en kilómetros
            km_to_deg = distancia_km / (earth_radius * 2 * 3.14159265359 / 360.0)

            queryset = queryset.annotate(
                lat_diff=ExpressionWrapper(
                    Radians(F('latitud') - latitud),
                    output_field=FloatField()
                ),
                lon_diff=ExpressionWrapper(
                    Radians(F('longitud') - longitud),
                    output_field=FloatField()
                ),
                a=ExpressionWrapper(
                    Sin(F('lat_diff') / 2) * Sin(F('lat_diff') / 2) +
                    Cos(Radians(latitud)) * Cos(Radians(F('latitud'))) *
                    Sin(F('lon_diff') / 2) * Sin(F('lon_diff') / 2),
                    output_field=FloatField()
                ),
                c=ExpressionWrapper(
                    2 * Sqrt(F('a')),
                    output_field=FloatField()
                ),
                distancia=ExpressionWrapper(
                    earth_radius * F('c'),
                    output_field=FloatField()
                )
            ).filter(distancia__lte=km_to_deg).order_by('distancia')

        return queryset

class SpaceView(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    filter_backends = [DjangoFilterBackend, SpaceFilter]