from django.db import models

# Create your models here.
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.db import models

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))

class User(AbstractUser):
    telephone = models.CharField(max_length=10)
    group = models.CharField(max_length=20)

    def __str__(self):
        return self.username
