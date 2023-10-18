from django.db import models
#from .models import User
#from .models import Event

class Ticket(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.TextField(null=False, blank=False, max_length=560)
    event = models.TextField(null=False, blank=False, max_length=560)
    image = models.ImageField(upload_to='tickets/', default='images/qr.png')


    class Meta:
        unique_together = ('user', 'event')
        
    def __str__(self):
        return f"Ticket by {self.user} on {self.event}"
