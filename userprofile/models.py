from django.db import models
from django.contrib.auth.models import User
from main_app.models import Fungi

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', default='default_profile.jpg', blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fungi = models.ForeignKey(Fungi, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'fungi')  # Ensure a user can only like a post once
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.username} liked {self.fungi.name}'
