from django.db import models


from events.models import Event
from user.models import User


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)  
    text = models.TextField(null=False, blank=False, max_length=560)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"Comment by {self.user} on {self.event} at {self.created_at}"