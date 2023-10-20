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


