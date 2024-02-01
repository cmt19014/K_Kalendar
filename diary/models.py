from django.db import models
from django.contrib.auth.models import User

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s entry on {self.date}"
