from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add any additional fields you want here
    pass

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField()

    def __str__(self):
        return self.question_text
