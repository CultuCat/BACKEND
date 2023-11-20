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


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()

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
    token, _ = Token.objects.get_or_create(user=user)
    serializer = PerfilSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['DELETE'])
def delete_perfil(request):
    try:
        user = get_object_or_404(Perfil, username=request.data['username'])
    except Perfil.DoesNotExist:
        return Response({'detail': 'Usuari no trobat'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({'detail': 'Usuari eliminat correctament'}, status=status.HTTP_200_OK)

class TagsPreferits(APIView):
    def delete(self, request, user_id, tag_name):
        try:
            user = Perfil.objects.get(id=user_id)
            tag = Tag.objects.get(nom=tag_name)

            user.tags_preferits.remove(tag)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Perfil.DoesNotExist:
            return Response({"error": f"El usuario {user.username} no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Tag.DoesNotExist:
            return Response({"error": f"El tag con ID {tag_name} no existe"}, status=status.HTTP_404_NOT_FOUND)

