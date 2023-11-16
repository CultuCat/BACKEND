from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer, TicketSerializer_byEvent, TicketSerializer_byUser
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend

class TicketsView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    models = Ticket
    #permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'user']
    
    apply_permissions = False

    def get_permissions(self):
        if self.action == 'create' and self.apply_permissions:
            return [IsAuthenticated]
        else:
            return []
        
    def get_serializer_class(self):
        user_param = self.request.query_params.get('user', None)
        event_param = self.request.query_params.get('event', None)

        # Determinar el serializador basado en los parámetros de la solicitud
        if user_param is not None and event_param is None:
            return TicketSerializer_byUser
        elif event_param is not None and user_param is None:
            return TicketSerializer_byEvent
        else:
            return TicketSerializer

    def create(self, request, *args, **kwargs):
        ticket = request.data.copy()
        ticket['user'] = 1 #request.user.id #1
        serializer = self.get_serializer(data=ticket)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
