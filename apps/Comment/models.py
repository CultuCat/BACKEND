from django.db import models

from config import settings
from api.bookings.models import Bookings
from api.users.models import Users


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=True, blank=True)  
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.booking} at {self.created_at}"
