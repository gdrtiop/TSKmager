from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    class Meta:
        db_table = 'Task'

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assigned = models.ForeignKey(to=User, on_delete=models.CASCADE)
    done = models.BooleanField(default=0)
    who_done = models.ForeignKey(to=User, on_delete=models.CASCADE)
    approved = models.ForeignKey(to=User, on_delete=models.CASCADE)
    deadline = models.DateTimeField


class Project(models.Model):
    class Meta:
        db_table = 'Project'

    name = models.CharField(max_length=150, default='Untitled project')
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    members = models.ManyToManyField(to=User)
    tasks = models.ManyToManyField(to=User)
