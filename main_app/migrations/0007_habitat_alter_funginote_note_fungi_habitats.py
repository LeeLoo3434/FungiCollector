# Generated by Django 4.1.6 on 2023-02-12 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_funginote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habitat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='funginote',
            name='note',
            field=models.TextField(verbose_name='note'),
        ),
        migrations.AddField(
            model_name='fungi',
            name='habitats',
            field=models.ManyToManyField(to='main_app.habitat'),
        ),
    ]
