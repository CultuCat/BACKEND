from django.db import models
from events.models import Event
from user.models import Perfil
import random

def get_random_image():
    IMAGE_CHOICES = [
        'https://static.vecteezy.com/system/resources/previews/002/258/271/large_2x/template-of-qr-code-ready-to-scan-with-smartphone-illustration-vector.jpg',
        'https://th.bing.com/th/id/OIP.T0ywp7K4Ke4LifNoo6n1zwHaFS?rs=1&pid=ImgDetMain',
        'https://www.elegantthemes.com/blog/wp-content/uploads/2019/05/How-to-create-a-QR-code-Elegant-Themes-Blog.png',
    ]
    return random.choice(IMAGE_CHOICES)

class Ticket(models.Model):
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False, blank=False, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)
    image = models.CharField(default=get_random_image, max_length=200)


    class Meta:
        unique_together = ('user', 'event')
        ordering = ['event__dataIni']
        
    def __str__(self):
        return f"Ticket by {self.user} on {self.event}"
