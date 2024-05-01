# Generated by Django 5.0.4 on 2024-04-22 16:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Untitled project', max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_project', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='members_project', to=settings.AUTH_USER_MODEL)),
                ('tasks', models.ManyToManyField(related_name='tasks_project', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Project',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('done', models.BooleanField(default=0)),
                ('approved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_task', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_task', to=settings.AUTH_USER_MODEL)),
                ('who_done', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_done_task', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Task',
            },
        ),
    ]
