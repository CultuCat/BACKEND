from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ticket
from discount.models import Discount
from .serializers import TicketSerializer
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend

from utility.new_discount_utils import verificar_y_otorgar_descuento

class TicketsView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
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

    def create(self, request, *args, **kwargs):
        ticket = {
            'user': 1,  #request.user.id #1
            'event': request.data.get('event')
        }
        serializer = self.get_serializer(data=ticket)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        #si se usa un descuento se marca como usado
        if request.data.get('discount') is not None:
            descuento = Discount.objects.get(codi=request.data.get('discount')) #si ja dejado hacer el post de entrada es porq ya se ha comprobado q el descuento existe y es válido
            # Cambia el valor de bool a True
            descuento.usat = True
            descuento.save()
            
        verificar_y_otorgar_descuento(ticket['user'], "Més esdeveniments", Ticket.objects.filter(user= ticket['user']).count())  
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        # ticket = request.data.copy()
        # ticket['user'] = 1 #request.user.id #1
        # serializer = self.get_serializer(data=ticket)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
