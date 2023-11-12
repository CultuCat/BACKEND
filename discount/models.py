from django.db import models
from user.models import User

class Discount(models.Model):
    codi = models.CharField(primary_key=True)
    userDiscount = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    NIVELL_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    nivellTrofeu = models.IntegerField(choices=NIVELL_CHOICES, null=False, blank=False)
    nomTrofeu = models.CharField(null=False, blank=False)
    usat = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['nomTrofeu', 'nivellTrofeu']
