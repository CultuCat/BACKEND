from django.db import models
from events.models import Event
from user.models import Perfil
import random

IMAGE_CHOICES = [
        'https://storage.cloud.google.com/cultucat_bucket/images/EncontradoQR.png',
        'https://storage.cloud.google.com/cultucat_bucket/images/NanoQR.png',
        'https://storage.cloud.google.com/cultucat_bucket/images/GolasoQR.png',
        'https://storage.cloud.google.com/cultucat_bucket/images/PatacasQR.png',
    ]

def get_random_image():
    return random.choice(IMAGE_CHOICES)


class Ticket(models.Model):
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False, blank=False, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)
    image = models.CharField(max_length=255, blank=True) #IMAGE_CHOICES[random.randint(0, len(IMAGE_CHOICES)-1)]
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = get_random_image()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['event__dataIni']
        
        
    def __str__(self):
        return f"Ticket by {self.user} on {self.event}"
