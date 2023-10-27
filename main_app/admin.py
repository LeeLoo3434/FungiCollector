from django.contrib import admin
# import your models here
from .models import Fungi, Comment

# Register your models here
admin.site.register(Fungi)
admin.site.register(Comment)

