from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    class Meta:
        db_table = 'Task'

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000, null=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author_task')
    assigned = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='assigned_task', null=True)
    done = models.BooleanField(default=0)
    who_done = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='who_done_task', null=True)
    approved = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    deadline = models.DateTimeField(null=True)


class Project(models.Model):
    class Meta:
        db_table = 'Project'

    name = models.CharField(max_length=150, default='Untitled project')
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author_project')
    members = models.ManyToManyField(to=User, related_name='members_project')
    tasks = models.ManyToManyField(to=Task, related_name='tasks_project')
    liked = models.BooleanField(default=0)


class Complaint(models.Model):
    class Meta:
        db_table = "Complaints"

    text = models.CharField(max_length=1000, default='')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000, default='')
    data = models.DateTimeField()