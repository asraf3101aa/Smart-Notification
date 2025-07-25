from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from thread.models.thread_models import Thread

User = get_user_model()

class Comment(models.Model):
    text = models.TextField(
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(300)
        ]
    ) 
    thread = models.ForeignKey(Thread, related_name='comments', on_delete=models.CASCADE)   
    created_by = models.ForeignKey(User, related_name='thread_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

