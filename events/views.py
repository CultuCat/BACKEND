from rest_framework import viewsets, status
from .models import Event
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
from rest_framework.decorators import action

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    models = Event
    permission_classes = [IsAuthenticatedOrReadOnly] 
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ['dataIni', 'nom', 'espai']

    def get_permission_classes(self):
        if self.action == 'create':
            return [IsAdmin()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == 'create':    
            return EventCreateSerializer
        return EventSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

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
        if ordering == 'espai':
            ordering = 'espai__nom'
        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('dataIni')
        
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