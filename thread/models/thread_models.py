from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator

User = get_user_model()

class Thread(models.Model):
    title = models.CharField(
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(100)
        ]
    )
    description = models.TextField(
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(300)
        ]
    )    
    created_by = models.ForeignKey(User, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
