# Generated by Django 5.0.7 on 2024-11-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_rename_picture_urls_project_project_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temporaryimage',
            old_name='uploaded_at',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='temporaryimage',
            name='session_key',
            field=models.CharField(max_length=255),
        ),
    ]