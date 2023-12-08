from django.db import models
from user.models import Perfil

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user_from = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False, blank=False, related_name='messages_from')
    user_to = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False, blank=False, related_name='messages_to')
    text = models.TextField(null=False, blank=False, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.user_from} to {self.user_to} at {self.created_at}"
