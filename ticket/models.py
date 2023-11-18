from django.db import models
from events.models import Event
from user.models import User

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(default='/images/qr.jpg')


    class Meta:
        unique_together = ('user', 'event')
        ordering = ['event__dataIni']
        
    def __str__(self):
        return f"Ticket by {self.user} on {self.event}"
