# Generated by Django 4.1.7 on 2023-02-25 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasks',
            old_name='creando',
            new_name='creado',
        ),
    ]
