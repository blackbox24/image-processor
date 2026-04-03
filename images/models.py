from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/uploads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"image: {self.pk}"
