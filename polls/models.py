from django.contrib.auth.models import AbstractUser
from django.db import models

class Machine(models.Model):
    STATUS_CHOICES = [
        ('OK', 'Operational'),
        ('Warning', 'Warning'),
        ('Fault', 'Fault'),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    collection = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FaultCase(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='faults')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=Machine.STATUS_CHOICES, default='Fault')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fault {self.id} - {self.machine.name}"

class FaultNote(models.Model):
    fault_case = models.ForeignKey(FaultCase, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='fault_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note on {self.fault_case.id} by {self.author}"

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Technician', 'Technician'),
        ('Repair', 'Repair'),
        ('Manager', 'Manager'),
        ('View-Only', 'View-Only'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} - {self.role}"
