from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Images(models.Model):
    user: models.ForeignKey[User] = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/uploads")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"image: {self.pk}"
