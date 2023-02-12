from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Fungi(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preferred_environment = models.CharField(max_length=100)
    edibility = models.CharField(max_length=100)
    date_collected = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('fungi_detail', kwargs={'pk': self.id})
    

class FungiNote(models.Model):
    note = models.TextField('note')
    fungi = models.ForeignKey(Fungi, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}:{self.note}'
