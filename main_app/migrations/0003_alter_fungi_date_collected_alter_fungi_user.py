# Generated by Django 4.1.6 on 2023-02-11 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0002_fungi_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fungi',
            name='date_collected',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='fungi',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
