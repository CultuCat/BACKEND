from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer, TicketSerializer_byEvent, TicketSerializer_byUser
from discount.models import Discount
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from events.models import Event
from user.models import Perfil, SpacePreferit, TagPreferit
from rest_framework.authentication import TokenAuthentication


from utility.new_discount_utils import verificar_y_otorgar_descuento

class TicketsView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'user']
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        else:
            return []
        
    def get_serializer_class(self):
        user_param = self.request.query_params.get('user', None)
        event_param = self.request.query_params.get('event', None)

        # Determinar el serializer basado en la solicitud
        if user_param is not None and event_param is None:
            return TicketSerializer_byUser
        elif event_param is not None and user_param is None:
            return TicketSerializer_byEvent
        else:
            return TicketSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
    
        ticket = {
            'user': request.user.id,
            'event': request.data.get('event')
        }
        serializer = self.get_serializer(data=ticket)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        event = Event.objects.get(id=ticket['event'])

        event_tags = event.tags.all()
        event_espai = event.espai

        user = Perfil.objects.get(id=ticket['user'])

        for tag in event_tags:
            tag_preferit, _ = TagPreferit.objects.get_or_create(tag=tag, user=user)
            tag_preferit.count += 1
            if not tag_preferit.show: tag_preferit.show = True
            tag_preferit.save()

        espai_preferit, _ = SpacePreferit.objects.get_or_create(space=event_espai, user=user)
        espai_preferit.count += 1
        if not espai_preferit.show: espai_preferit.show = True
        espai_preferit.save()

        #si se usa un descuento se marca como usado
        if request.data.get('discount') is not None:
            descuento = Discount.objects.get(codi=request.data.get('discount')) #si ja dejado hacer el post de entrada es porq ya se ha comprobado q el descuento existe y es válido
            # Cambia el valor de bool a True
            descuento.usat = True
            descuento.save()
            
        verificar_y_otorgar_descuento(ticket['user'], "Més esdeveniments", Ticket.objects.filter(user= ticket['user']).count())  
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   
    
