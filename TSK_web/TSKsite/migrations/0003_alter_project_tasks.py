# Generated by Django 5.0.4 on 2024-04-23 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TSKsite', '0002_project_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tasks',
            field=models.ManyToManyField(related_name='tasks_project', to='TSKsite.task'),
        ),
    ]
