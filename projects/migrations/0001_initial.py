# Generated by Django 5.0.7 on 2024-12-29 04:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('major_field', models.CharField(max_length=100)),
                ('sub_field', models.CharField(max_length=100)),
                ('skills', models.TextField(blank=True, null=True)),
                ('links', models.JSONField()),
                ('project_img', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_public', models.CharField(default='False', max_length=10)),
                ('liked_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.pofolouser')),
            ],
            options={
                'db_table': 'projects',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.pofolouser')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commented_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='projects.comment')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.pofolouser')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.project')),
            ],
        ),
    ]
