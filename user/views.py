from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from user.serializers import PerfilSerializer, PerfilShortSerializer, FriendshipRequestSerializer, FriendshipCreateSerializer, FriendshipAcceptSerializer
from user.models import Perfil, FriendshipRequest
from tags.models import Tag
from spaces.models import Space
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from user.permissions import IsAdmin


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ['id', 'puntuacio']

    filterset_fields = ['username']

    def get_serializer_class(self):
        if self.action == 'list':
            return PerfilShortSerializer
        elif self.action == 'send_friend_request':    
            return FriendshipCreateSerializer
        elif self.action == 'accept_friend_request': 
            return FriendshipAcceptSerializer
        return PerfilSerializer

    @action(methods=['GET', 'PUT'], detail=False)
    def profile(self, request):
        

        if self.request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': "El token d'autentificació no ha sigut donat."})


        if request.method == 'GET':
            profiles = Perfil.objects.all()
            response_data = []

            for profile in profiles:
                token, _ = Token.objects.get_or_create(user=profile.user)
                serializer = PerfilSerializer(instance=profile.user)
                
                user_data = {
                    'token': token.key,
                    'user': serializer.data
                }
                response_data.append(user_data)

            return Response(response_data)

        elif request.method == 'PUT':
            user = Token.objects.get(key=self.request.auth.key).user
            newImage = request.data.get('imatge', None)
            newBio = request.data.get('bio', None)

            if newImage is not None:
                user.perfil.imatge = newImage
            if newBio is not None:
                user.perfil.bio = newBio
            user.save()
            user.perfil.save()

        serializer = PerfilSerializer(user.perfil)
        return Response(status=status.HTTP_200_OK, data={*serializer.data, *{'message': "S'ha actualitzat el perfil"}})
    
    @action(detail=True, methods=['POST'])
    def send_friend_request(self, request, pk=None):
        sender_profile = self.get_object()
        receiver_id = request.data.get('to_user')
        receiver_profile = get_object_or_404(Perfil, id=receiver_id)

        created = sender_profile.send_friend_request(receiver_profile)
        if created:
            return Response({'detail': 'Solicitud de amistad enviada'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Ya tienes una solicitud de amistad de ese usuario'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def accept_friend_request(self, request, pk=None):
        request_id = request.data.get('id')
        friendship_request = get_object_or_404(FriendshipRequest, id=request_id)

        if (request.data.get('is_accepted') == True):
            friendship_request.accept()
            return Response({'detail': 'Solicitud de amistad aceptada'}, status=status.HTTP_200_OK)
        else:
            friendship_request.decline()
            return Response({'detail': 'Solicitud de amistad rechazada'}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['PUT'])
    def wants_to_talk_perfil(self,request,pk=None):
        perfil = self.get_object()
        wants_to_talk = request.data.get('wantsToTalk')

        perfil.wantsToTalk = wants_to_talk
        perfil.save()

        if (perfil.wantsToTalk == True):
            return Response({'detail': 'La resta dels usuaris poden parlar amb tu'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'La resta dels usuaris no poden parlar amb tu'}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['PUT'])
    def is_visible_perfil(self,request,pk=None):
        perfil = self.get_object()
        is_visible = request.data.get('isVisible')

        perfil.isVisible = is_visible
        perfil.save()

        if (perfil.isVisible == True):
            return Response({'detail': 'La resta dels usuaris et poden trobar'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'La resta dels usuaris no et poden trobar'}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['PUT'])
    def block_profile(self, request, pk=None):
        perfil = self.get_object()
        is_blocked = request.data.get('isBlocked')

        if request.user.is_staff:
            
            perfil.isBlocked = is_blocked
            perfil.save()

            if perfil.isBlocked == True:
                return Response({'detail': "L'usuari està bloquejat"}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "L'usuari no està bloquejat"}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No tens permisos per fer aquesta acció'}, status=status.HTTP_403_FORBIDDEN)

    
@api_view(['POST'])
def signup_perfil(request):
    serializer = PerfilSerializer(data=request.data)
    email = request.data.get('email')
    if Perfil.objects.filter(email=email).exists():
        return Response({'email: This email is already used'}, status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        user = Perfil.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_perfil(request):
    user = get_object_or_404(Perfil, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"L'usuari o el password no són correctes"}, status=status.HTTP_404_NOT_FOUND)
    if user.isBlocked:
        return Response({"detail": "L'usuari està bloquejat per l'administració"}, status=status.HTTP_403_FORBIDDEN)
    token, _ = Token.objects.get_or_create(user=user)
    serializer = PerfilSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data})



class TagsPreferits(APIView):
    def delete(self, request, user_id, tag_id):
        try:
            user = Perfil.objects.get(id=user_id)
            tag = Tag.objects.get(id=tag_id)

            user.tags_preferits.remove(tag)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Perfil.DoesNotExist:
            return Response({"error": f"El usuario {user.username} no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Tag.DoesNotExist:
            return Response({"error": f"El tag con ID {tag_id} no existe"}, status=status.HTTP_404_NOT_FOUND)
        
class SpacesPreferits(APIView):
    def delete(self, request, user_id, space_id):
        try:
            user = Perfil.objects.get(id=user_id)
            space = Space.objects.get(id=space_id)
            user.espais_preferits.remove(space)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Perfil.DoesNotExist:
            return Response({"error": f"El usuario {user.username} no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Tag.DoesNotExist:
            return Response({"error": f"El tag con ID {space_id} no existe"}, status=status.HTTP_404_NOT_FOUND)
        
