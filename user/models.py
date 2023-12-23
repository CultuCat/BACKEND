from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from tags.models import Tag
from spaces.models import Space
from enum import Enum
from storages.backends.gcloud import GoogleCloudStorage
from django.core.files.storage import default_storage
storage = GoogleCloudStorage()


class FriendshipRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey('Perfil', related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey('Perfil', related_name='friendship_requests_received', on_delete=models.CASCADE)
    is_answered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.is_answered = True
        self.is_accepted = True
        self.save()

    def decline(self):
        self.is_answered = True
        self.save()

class TagPreferit(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=("Tag preferit"), on_delete=models.CASCADE)
    user = models.ForeignKey('Perfil', verbose_name=("User amb tag preferit"), on_delete=models.CASCADE)
    count = models.IntegerField(null=False, default=0, verbose_name=_('Comptador de vegades'))
    show = models.BooleanField(default=True)

    @property
    def tags_info(self):
        return [
            {'id': self.tag.id, 'nom': self.tag.nom, 'count': self.count}
        ]

class SpacePreferit(models.Model):
    space = models.ForeignKey(Space, verbose_name=("Espai preferit"), on_delete=models.CASCADE)
    user = models.ForeignKey('Perfil', verbose_name=("User amb tag preferit"), on_delete=models.CASCADE)
    count = models.IntegerField(null=False, default=0, verbose_name=_('Comptador de vegades'))
    show = models.BooleanField(default=True)
    
    @property
    def espais_info(self):
        return [
            {'id': self.space.id, 'nom': self.space.nom, 'count': self.count}
        ]

class Perfil(User):
    usernameGoogle = models.CharField(max_length=150, null=True, verbose_name='Username pels usuaris de Google')
    imatge = models.ImageField(upload_to='images/',default='images/avatarDefault.png')
    imatge_url = models.CharField(null=True, verbose_name=('Imatge si es fa log in de Google'))
    bio = models.CharField(max_length=200, default="Hey there, I'm using CultuCat", null=True, blank=True, verbose_name=_('Bio'))
    puntuacio = models.IntegerField(null=False, default=0, verbose_name=_('Puntuacio'))
    isBlocked = models.BooleanField(default=False, verbose_name=_('Està bloquejat a la aplicacio'))
    wantsToTalk = models.BooleanField(default=True, verbose_name=_('La resta dels usuaris poden parlar amb ell'))
    isVisible = models.BooleanField(default=True,verbose_name=_('La resta dels usuaris el poden trobar'))
    wantsNotifications = models.BooleanField(default=True, verbose_name=_('Permet notificacions'))
    isGoogleUser = models.BooleanField(default=False, verbose_name=('L\'usuari és de Google'))

    class LanguageChoices(Enum):
        ENGLISH = 'en'
        SPANISH = 'es'
        CATALAN = 'cat'

    language = models.CharField(max_length=3, choices=[(language.value, language.name) for language in LanguageChoices], default=LanguageChoices.CATALAN.value)

    def get_imatge(self):
        if self.imatge_url and 'images/avatarDefault.png' == self.imatge.name:
            return self.imatge_url
        return default_storage.url(self.imatge.name)

    def send_friend_request(self, to_user):
        if not FriendshipRequest.objects.filter(from_user=self, to_user=to_user, is_accepted=True).exists() and \
            not FriendshipRequest.objects.filter(from_user=self, to_user=to_user, is_answered=False).exists() and \
            not FriendshipRequest.objects.filter(from_user=to_user, to_user=self, is_accepted=True).exists() and \
            not FriendshipRequest.objects.filter(from_user=to_user, to_user=self, is_answered=False).exists():
            FriendshipRequest.objects.create(from_user=self, to_user=to_user)
            return True
        return False
            
    def get_pending_friend_requests(self):
            return FriendshipRequest.objects.filter(to_user=self, is_answered=False)
    
    def get_pending_friend_requests_sent(self):
            return FriendshipRequest.objects.filter(from_user=self, is_answered=False)

    def get_friends(self):
            friends = []
            sent_requests = FriendshipRequest.objects.filter(from_user=self, is_answered=True, is_accepted=True)
            received_requests = FriendshipRequest.objects.filter(to_user=self, is_answered=True, is_accepted=True)

            for request in sent_requests:
                friends.append(request.to_user)

            for request in received_requests:
                friends.append(request.from_user)

            return friends
    
    def get_espais_preferits(self):
        espais_preferits = SpacePreferit.objects.filter(user=self, show=True)
        espais_info_list = []

        for espai_preferit in espais_preferits:
            espais_info_list.extend(espai_preferit.espais_info)

        return espais_info_list

    def get_tags_preferits(self):  
        tag_preferits = TagPreferit.objects.filter(user=self, show=True)
        tags_info_list = []

        for tag_preferit in tag_preferits:
            tags_info_list.extend(tag_preferit.tags_info)

        return tags_info_list
    
    def wants_to_talk_status(self, wants_to_talk):
        if wants_to_talk != self.wantsToTalk:
            self.wantsToTalk = wants_to_talk
            self.save()

    def is_visible_status(self, is_visible):
        if is_visible != self.isVisible:
            self.isVisible = is_visible
            self.save()

    @staticmethod
    def upload_image(file, filename):
        try:
            target_path = '/images/' + filename
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print("Failed to upload!")
