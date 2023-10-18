from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer

class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def retrieve(self, request, event_id, *args, **kwargs):
        # Check if a ticket exists for the currently logged-in user and the specified event
        user = self.request.user
        try:
            ticket = Ticket.objects.get(event=event_id, user=user)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        except Ticket.DoesNotExist:
            return Response({'detail': 'No ticket found for this event.'}, status=status.HTTP_404_NOT_FOUND)
