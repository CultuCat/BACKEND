from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from user.models import Perfil
from ticket.models import Ticket
from user.serializers import PerfilSerializer
from ticket.serializers import TicketSerializer
from user.permissions import IsAuthenticated

from social_django.utils import psa

from requests.exceptions import HTTPError



class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

    @action(methods=['GET', 'PUT'], detail=False)
    def profile(self, request):

        if self.request.auth is None:
            return Response(status=400, data={'error': "El token d'autentificació no ha sigut donat."})

        user = Token.objects.get(key=self.request.auth.key).user

        if request.method == 'PUT':
            newPassword = request.data.get('password', None)
            newImage = request.data.get('imatge', None)
            newBio = request.data.get('bio', None)

            if newPassword is not None:
                user.set_password(newPassword)
            if newImage is not None:
                user.perfil.imatge = newImage
            if newBio is not None:
                user.perfil.bio = newBio
            user.save()
            user.perfil.save()

        serializer = PerfilSerializer(user.perfil)
        return Response(status=200, data={*serializer.data, *{'message': "S'ha actualitzat el perfil"}})
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    




@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def SignIn_Google(request, backend):
    token = request.POST.get('access_token', None)
    if token is None:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': "El token d'accés no ha sigut donat."})
    try:
        user = request.backend.do_auth(token)
        print(request)
    except HTTPError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': {'token': "Token invalid", 'detail': str(e)}})


    if user:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            if user.perfil is None:
                Perfil.objects.create(user=user)
            serializer = PerfilSerializer(user.perfil)
            return Response(status=status.HTTP_200_OK, data={**serializer.data, 'token': token.key, 'created': created})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': "L'usuari ha esborrat el seu compte o ha sigut banejat per l'administrador"})

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': {'token': "Token invalid"}})
    

#get users by ticket
class TicketUsersView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, ticket_id=None):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Ticket no trobat'})

        users_with_ticket = Perfil.objects.filter(ticket=ticket.event)
        serializer = PerfilSerializer(users_with_ticket, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)