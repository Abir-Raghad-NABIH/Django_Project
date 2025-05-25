from django.db import models
from django.contrib.auth.models import User

class VoyageurProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.TextField(blank=True)
    documents = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"
