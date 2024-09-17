from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    stage_options = [
        (1, 'Pendientes'),   # backlog
        (2, 'Haciendo'),     # incomplete
        (3, 'En revision'),  # in review
        (4, 'Completado')    # completed
    ]
    index = models.IntegerField(default=0)
    name = models.CharField(max_length= 200)
    completed = models.BooleanField(default=False)
    stage = models.IntegerField(choices=stage_options, default=1)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)