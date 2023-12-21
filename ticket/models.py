from django.db import models
from events.models import Event
from user.models import Perfil
import random

IMAGE_CHOICES = [
        'images/EncontradoQR.png',
        'images/NanoQR.png',
        'images/GolasoQR.png',
        'images/PatacasQR.png',
    ]

def get_random_image():
    return random.choice(IMAGE_CHOICES)

class Ticket(models.Model):
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False, blank=False, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(default=get_random_image)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['event__dataIni']
        
    def __str__(self):
        return f"Ticket by {self.user} on {self.event}"