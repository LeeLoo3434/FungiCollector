from django.contrib import admin
# import your models here
from .models import Fungi, FungiNote

# Register your models here
admin.site.register(Fungi)
admin.site.register(FungiNote)

