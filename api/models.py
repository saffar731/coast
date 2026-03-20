from django.db import models

class StoreUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user_id_slug = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} | {self.user_id_slug}"