

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission 


def validate_file_extension(value):
    """Validator to ensure file extension is one of the allowed types. I have allowed pdf also """
    
    if not value.name.endswith(('.pptx', '.docx', '.xlsx' ,'.pdf')):
        raise ValidationError('File type is not allowed. Only pptx, docx, and xlsx are accepted.')

class Assignment(models.Model):
    doc = models.FileField(upload_to='assignments/', validators=[validate_file_extension])
    
    def save(self, *args, **kwargs):
       
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Assignment - {self.doc.name}"
    


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ops_user', 'Operation User'),
        ('client_user', 'Client User'),
    )
    user_type = models.CharField(max_length=12, choices=USER_TYPE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)
