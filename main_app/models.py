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
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_fungi', blank=True)


    def get_absolute_url(self):
        return reverse('fungi_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-date_collected']
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # User who added the comment
    content = models.TextField('content')  # renamed note to content
    fungi = models.ForeignKey(Fungi, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}:{self.content}'

