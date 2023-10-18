from django.db import models


# from config import settings
# from apps.bookings.models import Events
# from apps.users.models import Users


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    #event = models.ForeignKey(Events, on_delete=models.CASCADE, null=False, blank=False)  
    user = models.TextField(null=False, blank=False, max_length=560)
    event = models.TextField(null=False, blank=False, max_length=560)
    text = models.TextField(null=False, blank=False, max_length=560)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.event} at {self.created_at}"

