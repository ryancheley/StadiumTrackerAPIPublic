from django.db import models
from StadiumTrackerAPI import settings


class Content(models.Model):
    title = models.TextField()
    page_content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
