from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Fungi(models.Model):
    photo = models.ImageField(upload_to='fungi_photos/', default='default.jpg', blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    preferred_environment = models.CharField(max_length=100)
    edibility = models.BooleanField(default=False)  # True means edible, False means not
    date_collected = models.DateTimeField()
    identified = models.BooleanField(default=False)  # True means identified, False means not
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('fungi_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-date_collected']
class FungiNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # User who added the note
    note = models.TextField('note')
    fungi = models.ForeignKey(Fungi, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}:{self.note}'

