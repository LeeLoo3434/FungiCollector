# Generated by Django 4.2.6 on 2023-10-26 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0009_fungi_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fungi',
            options={'ordering': ['-date_collected']},
        ),
        migrations.RemoveField(
            model_name='fungi',
            name='habitats',
        ),
        migrations.AddField(
            model_name='fungi',
            name='identified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='funginote',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fungi',
            name='edibility',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Habitat',
        ),
    ]
