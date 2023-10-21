from django.db import models
from events.models import Event
from user.models import User

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tickets/', default='images/qr.png')


    class Meta:
        unique_together = ('user', 'event')
        
    def __str__(self):
        return f"Ticket by {self.user} on {self.event}"
