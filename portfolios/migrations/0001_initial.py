# Generated by Django 5.0.7 on 2024-12-28 06:39

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0004_delete_temporaryimage'),
        ('users', '0003_pofolouser_profile_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('major_field', models.CharField(max_length=100)),
                ('sub_field', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('skills', models.JSONField(default=list)),
                ('experiences', models.TextField()),
                ('invite_url', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=True)),
                ('views', models.IntegerField(default=0)),
                ('username', models.CharField(default='Unknown User', max_length=50)),
                ('related_projects', models.ManyToManyField(related_name='portfolios', to='projects.project')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='users.pofolouser')),
            ],
            options={
                'db_table': 'portfolios',
            },
        ),
    ]
