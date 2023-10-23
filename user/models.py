from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from cultucat import settings


def get_default_imatge():
    return settings.DEFAULT_IMATGE_PERFIL


class Perfil(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name=_('User'))
    imatge = models.ImageField(null=True, blank=True, default=get_default_imatge(), verbose_name=_('Imatge de perfil'))
    bio = models.CharField(max_length=200, default="", null=True, blank=True, verbose_name=_('Bio'))
    puntuacio = models.IntegerField(null=False, default=0, verbose_name=_('Puntuacio'))
    isBlocked = models.BooleanField(default=False, verbose_name=_('Està bloquejat a la aplicacio'))
    wantsToTalk = models.BooleanField(default=True, verbose_name=_('La resta dels usuaris poden parlar amb ell'))
    isVisible = models.BooleanField(default=True,verbose_name=_('La resta dels usuaris el poden trobar'))
    isAdmin = models.BooleanField(default=False,verbose_name=_("L'usuari es administrador"))

