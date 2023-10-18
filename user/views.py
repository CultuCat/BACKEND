from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Perfil
from .serializers import PerfilSerializer

from social_django.utils import psa

from django.conf import settings

from requests.exceptions import HTTPError


@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def SignIn_Google(request, backend):
    token = request.data.get('access_token')
    user = request.backend.do_auth(token)
    print(request)
    if user:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            if user.perfil is None:
                Perfil.objects.create(user=user)
            serializer = PerfilSerializer(user.perfil)
            return Response(status=200, data={**serializer.data, 'token': token.key, 'created': created})
        return Response(status=400, data={'errors': 'User deleted their account or was banned by an administrator.'})
    else:
        return Response(
            {
                'errors': {
                    'token': 'Invalid token'
                    }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )



@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def SignIn_Google(request, backend):
    token = request.POST.get('access_token', None)
    if token is None:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'No access_token was provided'})
    try:
        user = request.backend.do_auth(token)
        print(request)
    except HTTPError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': {'token': 'Invalid token', 'detail': str(e)}})


    if user:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            if user.perfil is None:
                Perfil.objects.create(user=user)
            serializer = PerfilSerializer(user.perfil)
            return Response(status=status.HTTP_200_OK, data={**serializer.data, 'token': token.key, 'created': created})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': 'User deleted their account or was banned by an administrator.'})

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': {'token': 'Invalid token'}})