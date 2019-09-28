from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    twitter_user = models.CharField(max_length=15, blank=True, null=True)
    instagram_user = models.CharField(max_length=30, blank=True, null=True)

