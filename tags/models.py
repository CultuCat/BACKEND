from django.db import models

class Tag(models.Model):
<<<<<<< Updated upstream
    id = models.AutoField(primary_key=True)
    nom = models.CharField(null=True, unique=True)
=======
    nom = models.CharField(primary_key=True)
>>>>>>> Stashed changes

    @classmethod
    def get_or_createTag(cls, nom):
        try:
            tag = cls.objects.get(nom=nom)
        except cls.DoesNotExist:
            tag = cls(nom=nom)
            tag.save()
        return tag