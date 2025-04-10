from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# 用户角色扩展
class Profile(models.Model):
    ROLE_CHOICES = [
        ('Technician', 'Technician'),
        ('Repair', 'Repair'),
        ('Manager', 'Manager'),
        ('View-only', 'View-only'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# 故障报告模型
class FaultCase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')
    ])

# 故障图片模型
class FaultImage(models.Model):
    fault_case = models.ForeignKey(FaultCase, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fault_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Machine(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.location}"
