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
        num_objs = request.query_params.get('num_objs')

        if latitud and longitud and num_objs:
            latitud = float(latitud)
            longitud = float(longitud)
            num_objs = int(num_objs)

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
                    6378 * F('c'),  # Usar radio de la Tierra de 6378 km
                    output_field=FloatField()
                )
            ).order_by('distancia')[:num_objs]

        return queryset


class SpaceView(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    filter_backends = [DjangoFilterBackend, SpaceFilter]

    def get_permissions(self):
            return []