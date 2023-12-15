from rest_framework import viewsets, status
from .models import Event
from user.models import TagPreferit, SpacePreferit
from .serializers import EventSerializer, EventListSerializer, EventCreateSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from user.permissions import IsAdmin
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from user.permissions import IsAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import action
from geopy.distance import geodesic
from django.utils import timezone
from datetime import datetime, timedelta
from ticket.models import Ticket
from django.db.models import Count

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    models = Event
    permission_classes = [IsAuthenticatedOrReadOnly] 
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ['dataIni', 'nom']

    def get_permission_classes(self):
        if self.action == 'create':
            return [IsAdmin()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'home' or self.action == 'today' or self.action == 'this_week':
            return EventListSerializer
        if self.action == 'list':
            latitud = self.request.query_params.get('latitud')
            longitud = self.request.query_params.get('longitud')
            distancia = self.request.query_params.get('distancia')

            if latitud and longitud and distancia:
                return EventSerializer
            else:
                return EventListSerializer
        elif self.action == 'create':    
            return EventCreateSerializer
        return EventSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        today = timezone.now().date()
        queryset = queryset.filter(Q(dataIni__gte=today) | Q(dataFi__gte=today))

        latitud = request.query_params.get('latitud')
        longitud = request.query_params.get('longitud')
        distancia = request.query_params.get('distancia')
        data_min = request.query_params.get('data_min')
        data_max = request.query_params.get('data_max')

        if data_min:
                data_min = datetime.strptime(data_min, '%d-%m-%Y')
                data_min = timezone.make_aware(data_min, timezone.get_current_timezone())
                queryset = queryset.filter(dataIni__gte=data_min)

        if data_max:
            data_max = datetime.strptime(data_max, '%d-%m-%Y')
            data_max = timezone.make_aware(data_max, timezone.get_current_timezone())
            queryset = queryset.filter(dataIni__lte=data_max)
        
        if latitud and longitud and distancia:
            latitud = float(latitud)
            longitud = float(longitud)
            distancia = float(distancia)

            queryset = [
                event for event in queryset
                if geodesic((latitud, longitud), (event.latitud, event.longitud)).km <= distancia
            ]

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        query = self.request.query_params.get('query', None)
        
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) | Q(espai__nom__icontains=query)
            )

        espai_ids = self.request.query_params.getlist('espai', [])
        if espai_ids:
            queryset = queryset.filter(espai__id__in=espai_ids)

        tag_ids = self.request.query_params.getlist('tag', [])
        if tag_ids:
            queryset = queryset.filter(tags__id__in=tag_ids)

        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering).distinct()
        else:
            queryset = queryset.order_by('dataIni').distinct()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff or not request.user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        event_data = request.data.copy()

        # Per asegurar-se que l'id no es repeteix, agafarem el mes antic i li restarem 1
        last_event = Event.objects.all().order_by('id').first()
        if last_event:
            id = last_event.id - 1
        else:
            id = 99999999999
        event_data['id'] = id

        event = Event.create_event(event_data)

        serializer = self.get_serializer(event)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['GET'])
    def home(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        today = timezone.now().date()
        queryset = queryset.filter(Q(dataIni__gte=today) | Q(dataFi__gte=today))
        user = request.user

        if not user.is_authenticated:
            queryset = queryset.order_by('-dataIni')
            events = queryset[:20]
            serializer = self.get_serializer(events, many=True)
            return Response(serializer.data)

        favorite_tags = TagPreferit.objects.filter(user=user).values_list('tag_id', flat=True)
        favorite_espais = SpacePreferit.objects.filter(user=user).values_list('space_id', flat=True)

        if not favorite_tags and not favorite_espais:
            queryset = queryset.order_by('-dataIni')
            events = queryset[:20]
            serializer = self.get_serializer(events, many=True)
            return Response(serializer.data)

        queryset = queryset.filter(Q(tags__id__in=favorite_tags) | Q(espai__id__in=favorite_espais))

        user_ticket_events = Ticket.objects.filter(user=user).values_list('event__id', flat=True)
    
        if user_ticket_events:
            queryset = queryset.exclude(id__in=user_ticket_events)

        queryset = queryset.order_by('dataIni').distinct()
        events = queryset[:20]
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def today(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        today = timezone.now().date()
        queryset = queryset.filter(dataIni=today)
        queryset = queryset.order_by('dataIni').distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def this_week(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        today = timezone.now().date()
        six_days_later = today + timezone.timedelta(days=6)

        queryset = queryset.filter(dataIni__range=[today, six_days_later]).order_by('dataIni').distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def free(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        today = timezone.now().date()
        queryset = queryset.filter(Q(dataIni__gte=today) | Q(dataFi__gte=today))

        queryset = queryset.filter(preu="Gratuït").order_by('dataIni').distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def popular(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        today = timezone.now().date()
        queryset = queryset.filter(Q(dataIni__gte=today) | Q(dataFi__gte=today))

        queryset = queryset.annotate(num_tickets=Count('ticket__id')).order_by('-num_tickets', 'dataIni')

        events = queryset[:20]
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)