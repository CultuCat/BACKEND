from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from user.serializers import PerfilSerializer, PerfilShortSerializer, FriendshipRequestSerializer, FriendshipCreateSerializer, FriendshipAcceptSerializer, PerfilCreateSerializer
from user.models import Perfil, FriendshipRequest, TagPreferit, SpacePreferit
from tags.models import Tag
from spaces.models import Space
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.core.exceptions import ObjectDoesNotExist

from utility.new_discount_utils import verificar_y_otorgar_descuento
import requests
from django.core.files.base import ContentFile


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id', 'puntuacio']
    filterset_fields = ['username']

    def get_serializer_class(self):
        if self.action == 'list':
            return PerfilShortSerializer
        elif self.action == 'signup_perfil':
            return PerfilCreateSerializer
        elif self.action == 'send_friend_request':
            return FriendshipCreateSerializer
        elif self.action == 'accept_friend_request':
            return FriendshipAcceptSerializer
        return PerfilSerializer

    def get_parser_classes(self):
        if self.action == 'update':
            return [MultiPartParser]
        else:
            return super().get_parser_classes()

    def update(self, request, pk=None):
        perfil = self.get_object()
        new_username = request.data.get('username', None)
        new_first_name = request.data.get('first_name', None)
        new_image = request.FILES.get('imatge', None)
        new_bio = request.data.get('bio', None)

        if request.user.id != int(pk):
            return Response({'detail': 'No tens permisos per fer aquesta acció'}, status=status.HTTP_403_FORBIDDEN)

        if newImage is not None:
            perfil.imatge = newImage
            Perfil.upload_image(newImage, newImage.name)

        if newBio is not None:
            perfil.bio = newBio

        perfil.save()

        serializer = PerfilSerializer(perfil)
        return Response({'data': serializer.data, 'message': "S'ha actualitzat el perfil"}, status=status.HTTP_200_OK)

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
            
            #se mira si el q envía cumple el trofeo
            verificar_y_otorgar_descuento(friendship_request.from_user_id, "Popular", FriendshipRequest.objects.filter(from_user=friendship_request.from_user_id, is_accepted=True).count()+FriendshipRequest.objects.filter(to_user=friendship_request.from_user_id, is_accepted=True).count())  
            #se mira si el user al q le envían cumple el trofeo
            verificar_y_otorgar_descuento(friendship_request.to_user_id, "Popular", FriendshipRequest.objects.filter(from_user=friendship_request.to_user_id, is_accepted=True).count()+FriendshipRequest.objects.filter(to_user=friendship_request.to_user_id, is_accepted=True).count())   
            
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
    def wants_notifications_perfil(self,request,pk=None):
        perfil = self.get_object()
        wants_notifications = request.data.get('wantsNotifications')

        perfil.wantsNotifications = wants_notifications
        perfil.save()

        if (perfil.wantsNotifications == True):
            return Response({'detail': 'Rebràs notificacions de l\'aplicació'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No rebràs notificacions de l\'aplicació'}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['PUT'])
    def put_language(self, request, user_id=None):
        id_user = self.kwargs.get('user_id')
        try:
            perfil = Perfil.objects.get(id=id_user)
        except Perfil.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.data.get('language')

        try:
            perfil.language = Perfil.LanguageChoices(language).value
            perfil.save()
        except ValueError:
            return Response({'detail': 'Idioma no vàlid'}, status=status.HTTP_400_BAD_REQUEST)

        if perfil.language == 'en':
            return Response({'detail': 'Now CultuCat is in english'}, status=status.HTTP_200_OK)
        elif perfil.language == 'es':
            return Response({'detail': 'Ahora CultuCat está en castellano'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Ara CultuCat està en català'}, status=status.HTTP_200_OK)

        
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
    email = request.data.get('email')
    if Perfil.objects.filter(email=email).exists():
        return Response({'email: This email is already used'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data

    data['wantsNotifications'] = True
    data['language'] = Perfil.LanguageChoices("cat").value
    serializer = PerfilCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        user = Perfil.objects.get(username=data['username'])
        if user.isGoogleUser:
            user.usernameGoogle = user.username
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        serializer = PerfilSerializer(instance=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_perfil(request):
    isGoogleUser = request.data.get('isGoogleUser')
    if isGoogleUser:
        user = get_object_or_404(Perfil, usernameGoogle=request.data['username'])
    else:
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

            tag_preferit = TagPreferit.objects.get(user=user, tag=tag)
            tag_preferit.show = False
            tag_preferit.save()

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
            
            espai_preferit = SpacePreferit.objects.get(user=user, space=space)
            espai_preferit.show = False
            espai_preferit.save()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Perfil.DoesNotExist:
            return Response({"error": f"El usuario {user.username} no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Tag.DoesNotExist:
            return Response({"error": f"El tag con ID {space_id} no existe"}, status=status.HTTP_404_NOT_FOUND)
        
