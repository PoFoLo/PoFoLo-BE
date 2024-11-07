# Generated by Django 5.0.7 on 2024-11-07 03:04

import django.db.models.deletion
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PofoloUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kakao_id', models.CharField(max_length=50, unique=True)),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('education', models.CharField(max_length=50)),
                ('education_is_public', models.BooleanField(default=True)),
                ('main_field', models.CharField(choices=[('plan', 'plan'), ('design', 'design'), ('develop', 'develop')], default='기획', max_length=10)),
                ('phone_num', models.CharField(blank=True, max_length=15, null=True)),
                ('phone_num_is_public', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('email_is_public', models.BooleanField(default=False)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('links', models.JSONField(blank=True, null=True)),
                ('availability', models.JSONField(blank=True, default=users.models.get_default_availability, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pofolo_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
