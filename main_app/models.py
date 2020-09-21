from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Sneaker(models.Model):
    name = models.CharField(max_length=30)
    style = models.CharField(max_length=30)
    colorway = models.CharField(max_length=30)
    price = models.IntegerField()
    release = models.DateField()
    condition = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detail', kwargs={'sneaker_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for sneaker_id: {self.sneaker_id} @{self.url}"