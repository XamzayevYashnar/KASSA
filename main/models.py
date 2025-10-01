from django.db import models

# Create your models here.

class Barcod(models.Model):
    code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code