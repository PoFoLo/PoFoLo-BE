# Generated by Django 5.0.7 on 2024-12-27 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pofolouser',
            name='profile_img',
        ),
    ]
