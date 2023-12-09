from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from .pusher import pusher_client

from utility.new_discount_utils import verificar_y_otorgar_descuento

class MessageViewSet(viewsets.ModelViewSet):
    
    def get(self, request):
        user_to = request.query_params.get('user1')
        user_from = request.query_params.get('user2')

        if user_to and user_from:
            # Intenta obtener los mensajes en ambas direcciones
            queryset = Message.objects.filter(user_to=user_to, user_from=user_from) | Message.objects.filter(user_to=user_from, user_from=user_to)
            queryset = queryset.order_by('created_at')
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Debes proporcionar los parámetros 'user_to' y 'user_from' en la consulta."}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        # Validar y guardar el mensaje en la base de datos
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()

            # Enviar notificación a través de Pusher solo si se creó correctamente
            pusher_client.trigger('chat', 'message', {
                'user_from': message.user_from.id,
                'user_to': message.user_to.id,
                'text': message.text,
            })
            
            verificar_y_otorgar_descuento(message.user_from.id, "Xerraire", Message.objects.filter(user_from= message.user_from.id).count()) 

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    