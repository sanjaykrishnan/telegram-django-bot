from django.db import models

# Create your models here.


class ChatUserData(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    stupid = models.PositiveIntegerField(default=0)
    fat = models.PositiveIntegerField(default=0)
    dumb = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
