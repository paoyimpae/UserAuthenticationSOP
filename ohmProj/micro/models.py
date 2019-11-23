from django.db import models

# Create your models here.
from django.contrib.auth.models import Group

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))
