from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Perfil(User):
    imatge = models.CharField(default='https://www.calfruitos.com/es/fotos/pr_223_20190304145434.png')    
    bio = models.CharField(max_length=200, default="Hey there, I'm using CultuCat", null=True, blank=True, verbose_name=_('Bio'))
    puntuacio = models.IntegerField(null=False, default=0, verbose_name=_('Puntuacio'))
    isBlocked = models.BooleanField(default=False, verbose_name=_('Està bloquejat a la aplicacio'))
    wantsToTalk = models.BooleanField(default=True, verbose_name=_('La resta dels usuaris poden parlar amb ell'))
    isVisible = models.BooleanField(default=True,verbose_name=_('La resta dels usuaris el poden trobar'))


