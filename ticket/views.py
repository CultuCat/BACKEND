from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend

class TicketsView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'event__id': ['exact', 'in'],
        'user__id': ['exact', 'in']
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id #1
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
